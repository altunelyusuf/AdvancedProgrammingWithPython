#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 14 (Excel Spreadsheets) on the CME classroom standard.

Same regime as chapters 10 to 13: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them,
labelled with their line numbers) with their results as Python printed them. Every console result and program transcript comes
from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with openpyxl 3.1.5); the speaker notes are
prose for the reader and carry only what the chapter's RDODI research package (03-materials/ch14/rdodi,
sen0414_ch14_rdodi_data_v1_0_1.py, findings F1 to F14), its records (08-tooling/ch14-page/*.json) or a program of this deck
established.

What this chapter adds against chapter 13: the eight narrative diagrams of the chapter (sen0414_ch14_diagrams_v1_0_0.py, grounding
0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py, the chapter 13 drawer with a state diagram whose boxes can be
sized) and checked by diagram_check_v1_0_0.py; one table (the county tally of Project 9) and one chart (the ten cells a bar chart
reads) are native PowerPoint objects whose data the deck check computes again; no photograph is used, because the research found
none it could fetch and licence (sen0414_ch14_stories_v1_0_0.py says why); three of the six stories are slides and three are told in
the notes, as chapter 13 told two of its six.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json and links_v1_0_0.json beside itself; needs rdflib)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diagram_shapes_v1_0_0 as DS


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories4141", os.path.join(HERE, "..", "sen0414_ch14_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams4141", os.path.join(HERE, "..", "sen0414_ch14_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi4141", os.path.join(HERE, "..", "sen0414_ch14_rdodi_data_v1_0_1.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * CW), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in (fs %.1f)" % (group, w, fs))
    L = lines_of(rr)
    h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.0725:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i > a and last in l)
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


def tw(pname, fs=7.0):
    """The panel width the transcript of a program needs on its own at fs points."""
    t = PROGS[pname]["transcript"].split("\n")
    return round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)


def prog(pname, x, y, w, fs=7.0, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'), as
    program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
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
    h = round(L * fs * 1.23 / 72.0 + 0.30 + 0.02 * max(0, L - 1), 2)
    label = "program %s, lines %d to %d of %d - Python %s" % (pname, a, b, len(all_lines), PYV)
    if len(label) > (w - 0.1) / 0.0725:
        label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: caption %r is too long for a %.2f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, fs=7.0, label="what the run printed"):
    """The transcript of a program in a panel of its own. With a label of the form 'transcript of program <name>' the panel is
    re-run by program_check and must equal the recording; with another label it is the transcript of a program whose
    excerpt is on the slide, which the program check also requires to be on that slide."""
    out = PROGS[pname]["transcript"]
    t = out.split("\n")
    need = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, w, fs, need))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: label %r is too long for a %.2f in panel" % (label, w))
    L = len(t)
    h = round(L * fs * 1.23 / 72.0 + 0.30 + 0.02 * max(0, L - 1), 2)
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": out,
            "outLabel": "prints", "label": label}


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


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap


S = []
SHOWN = {}  # diagram id -> slide number


def content(title, sub, items, notes, take, lede=None):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 53:
        raise SystemExit("REFUSED: title %r is longer than 53 characters" % title)
    if len(sub) > 92:
        raise SystemExit("REFUSED: subtitle %r is longer than the line it is set on" % sub)
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.85, 4.5, fs=10.5)
S.append({"kind": "title", "title": "Chapter 14: Excel Spreadsheets",
          "sub": "How a program reads and writes workbooks: openpyxl, cells, formulas, formatting, charts and two projects",
          "items": [c1],
          "notes": "Until this chapter a program's data lived in text files and on web pages. Chapter 14 turns to the file that "
                   "offices keep their numbers in: a program can open an Excel workbook, take its sheets and cells, count and add "
                   "what it finds, write new workbooks with formulas, fonts, merged cells, frozen panes and charts, and save the "
                   "result under a new name. This deck follows the chapter in that order and adds what the chapter leaves out, "
                   "which is what a formula does when no spreadsheet program has calculated it, why looking at a cell changes the "
                   "sheet, the places where the book's listings and files differ from what runs today, and the safe way to open a "
                   "file one did not make. Every example was run under Python 3.14.6 on Ubuntu with openpyxl 3.1.5, the newest "
                   "stable release on 12 October 2026, and the result printed beside it is the result that run gave. The book's "
                   "three Excel files are not part of this repository, so each program first makes a stand-in with the same "
                   "sheets, columns and formulas; the two projects were also run whole on the real files of the book's online "
                   "materials, and the one program marked live downloaded example3.xlsx from the book's site.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % (sum(len(v) for v in G.values()) - 0),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV]}],
        "The first question is the chapter's spine. A workbook is a file, a sheet is a page of it, a cell is one box of that page, "
        "and openpyxl gives each its own object: Workbook, Worksheet, Cell, and beside them a Font for a style, a string for a "
        "formula, a Reference and a Series and a BarChart for a chart. What the question asks for is what each object keeps of "
        "what the spreadsheet application stored, and the answer the deck gives is that values and formulas are kept, while the "
        "results of formulas, the way fonts and charts are drawn and the position of the window are not calculated or drawn by "
        "Python. The second question is the watch-out of the deck. The chapter's examples are sound and its two projects run on "
        "the real files, but the two Python scripts that ship with the files are in the style of the second edition and do not "
        "run, one sentence about the order of the arguments of Reference is backwards, and a few typeset marks and practice "
        "questions need a note, so each slide says where a printed line differs and on what evidence. The chips give the size of "
        "the chapter as this deck covers it: six branches, the topics beneath them, the console rows and programs that were run, "
        "and the eight diagrams.",
        "Know what each object keeps; then check what the book printed.")

# ---- 4 openpyxl and the xlsx file + use cases ------------------------------------------------------------------------
c, bot = con("library", 0.5, 1.5, 5.0, fs=8.5, label="openpyxl is a package; an .xlsx file is a zip of XML parts")
dg, dcap = diagram("WhatOpenpyxlCanDo", "usecases", (5.65, 1.45, 3.9, 3.15), fs=8)
content("openpyxl and the .xlsx file", "A third-party library that reads and writes the zip of XML parts Excel saves",
        [c, dg, dcap,
         card("Only this one reads and writes", "XlsxWriter writes .xlsx files but cannot read or modify one; xlrd 2 reads only the old "
              ".xls format. A file named .xls or .txt is refused with InvalidFileException.", 0.5, round(bot + 0.05, 2), 5.0, round(4.95 - bot - 0.05, 2), fs=10.5)],
        "openpyxl is a third-party package and not part of Python. Its newest stable release on 12 October 2026 was 3.1.5, "
        "uploaded on 28 June 2024, its one dependency is et-xmlfile, and the same program printed the same results under every "
        "release of Python 3.14 from 3.14.0 to 3.14.6 and under 3.13 and 3.12, with no warning even when warnings were turned into "
        "errors. An .xlsx file is a zip of XML parts, so the console saves an empty workbook into memory and counts nine parts, two "
        "of them the workbook and its first sheet. The use-case diagram lists what a program can do through the module: open a "
        "workbook and read its cells, create and remove sheets, write values and formulas, set fonts, merge cells and freeze "
        "panes, and add a chart. XlsxWriter writes .xlsx files but cannot read or modify one, and xlrd 2.0.2 reads only the "
        "historical .xls format, which is why openpyxl is the module of the chapter. load_workbook judges a file by its name "
        "before reading it: a name ending .xls or .txt is refused with InvalidFileException, and one ending .xlsx or .xlsm is read "
        "whatever name the bytes had when they were written. The library has a story of its own. Its documentation says it was "
        "born from the lack of a Python library to read and write the Office Open XML format natively, initially based on "
        "PHPExcel, by Eric Gazoni and Charlie Clark; the first upload to the Python Package Index, openpyxl 1.1.0, is dated "
        "11 August 2010, and the project describes itself as maintained by volunteers in their spare time. Because the project is "
        "quiet, a course should say which release it ran, and this deck ran 3.1.5. These accounts rest on the openpyxl "
        "documentation and the PyPI record of the package, read on 12 October 2026.",
        "openpyxl reads and writes .xlsx; say which release you ran.")

# ---- 5 story: OOXML ------------------------------------------------------------------------------------------------
content("The .xlsx format, a standard since 2006", STORY["OoxmlStandard2006"]["when"],
        [card("Ecma International and ISO", "Microsoft submitted documentation of its Office Open XML formats to Ecma International. "
              "ECMA 376 was approved in December 2006, and approval as ISO/IEC 29500 followed in early 2008.",
              0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Dec 2005: Ecma sets up committee TC45",
             "Dec 2006: ECMA 376 approved",
             "Early 2008: ISO/IEC 29500 approved",
             "An .xlsx is SpreadsheetML in a ZIP package"]},
         factrow("OoxmlStandard2006")],
        story_notes("OoxmlStandard2006"),
        "An .xlsx file is a documented zip of XML that any program may read.")

# ---- 6 sheets + diagram 1 ---------------------------------------------------------------------------------------------
dg, dcap = diagram("FromFileToCellValue", "activity", (0.5, 1.45, 5.3, 3.1),
                   grid={"load": (0, 0), "sheet": (0, 1), "how": (0, 2), "name": (0, 3), "nums": (1, 2), "value": (0, 4)},
                   cols=[(0.0, 2.9), (3.8, 1.5)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 5},
                   routes={("start", "load"): "h", ("nums", "value"): "vh"}, fs=8, nh=0.46, dh=0.46)
c, bot = con("sheets", 5.95, 1.5, 3.55, fs=9, label="a workbook, its sheets, a missing name", cap=True)
content("From a file to the value of a cell", "load_workbook() gives a Workbook; a name picks the Worksheet; two ways pick the Cell",
        [dg, dcap, c,
         {"t": "foot", "x": 5.95, "y": round(bot + 0.04, 2), "w": 3.55, "h": 0.5, "fs": 9.5,
          "body": "A sheet name that does not exist raises KeyError. Run on a small workbook built in memory, because example3.xlsx is not here."}],
        "This is the chapter's own review in seven steps. openpyxl.load_workbook() reads an .xlsx file and returns a Workbook "
        "object that stands for the whole file, a bit as a File object stands for an opened text file. The sheetnames attribute is "
        "the list of sheet names in the order of the tabs, and wb.active is the sheet that was on top when the file was saved; a "
        "workbook made in memory has its first sheet active. A Worksheet is got by its name in square brackets like a dictionary "
        "key, and a name that does not exist raises KeyError with the message printed. The one choice in the diagram is how the "
        "cell is named, by its letter and row number, as in sheet['A1'], or by two integers that start at 1, as in "
        "sheet.cell(row=1, column=2), which suits a loop; a row or column of 0 is refused with ValueError. The Cell's value "
        "attribute is the last step. The console builds a workbook with a second sheet in memory, saves it to a BytesIO object and "
        "loads it again, because the book's example3.xlsx is not in this repository; the same calls were run on the real file "
        "downloaded from the book's site, which the last slides show. One caution comes from the files that ship with the book: "
        "its script readCensusExcel.py still calls wb.get_sheet_by_name, which only draws a DeprecationWarning, and "
        "sheet.get_highest_row(), which no longer exists, so it stops with AttributeError; the chapter's own listing uses wb[...] "
        "and max_row and runs.",
        "A workbook holds sheets, a sheet holds cells; pick by name or by number.")

# ---- 7 cells ------------------------------------------------------------------------------------------------------------
c1, b1 = con("cells", 0.5, 1.5, 5.0, fs=8, label="cells by name and by number, slices, letters, dates")
c2, b2 = con("touch", 5.7, 1.5, 3.8, fs=8.5, label="looking at a cell creates it")
content("Cells, ranges and column letters", "By name or by number; one cell or a slice; and what merely looking at a cell does",
        [c1, c2,
         card("A loop that only looks", "A touched cell adds a row of None to Project 9's loop. On the real census file the book's cell loop "
              "peaked at 114 MB of traced memory; read_only iter_rows at 11 MB.",
              5.7, round(b2 + 0.05, 2), 3.8, round(4.95 - b2 - 0.05, 2), fs=9, accent="slate")],
        "A cell is got by its name in square brackets, its value is in the value attribute, columns start at A and rows at 1. A "
        "slice of two cell names gives a tuple of rows, each a tuple of the cells of that row, even when the range is a single "
        "row, which is why the console reads the values with a nested list. max_row and max_column are integers, and the column "
        "is a number and not the letter Excel shows; get_column_letter and column_index_from_string convert, 27 being AA and 900 "
        "being AHP. They accept columns up to ZZZ, number 18278, which is beyond the last column of Excel, XFD, number 16384, so "
        "they do not apply the limit of the application. The right-hand console shows the side effect the chapter does not "
        "mention. A worksheet starts with no cells and creates one the first time it is asked for, so cell(row=40, column=1) "
        "raises max_row to 40, makes the dimensions A40:A40, and a later read of A2 gives None, on which arithmetic raises "
        "TypeError. The sheet's size is therefore what was touched, not what was typed, and the same holds for int(None) in the "
        "loop of Project 9. Dates are numbers with a date format; openpyxl gives datetime values back, a date written as a date "
        "comes back as a datetime and a text that looks like a date stays text, and every cell has a one-letter data type: n, s, "
        "b, d or f. Two stories sit behind this. Excel was announced for the Macintosh on 2 May 1985 at Tavern on the Green in New "
        "York by Steve Jobs of Apple and Bill Gates, went on sale on 30 September 1985, and still treats 29 February 1900 as a "
        "day, a bug that began in Lotus 1-2-3 and was kept on purpose for compatibility, so the file format keeps the habits "
        "and the bugs of its program; that account rests on the Wikipedia article on Microsoft Excel and its sources. And in 2016 "
        "Ziemann, Eren and El-Osta found that Excel with its default settings turns gene symbols such as SEPT2 into dates, with "
        "errors in 987 files from 704 articles, 19.6 percent of the published articles with gene lists in the journals they "
        "selected, in Genome Biology 17, 177; a symbol written into a cell by openpyxl as a string keeps the data type s and no "
        "date is made of it.",
        "Looking at a cell creates it, so max_row counts what was touched.")

# ---- 8 story: VisiCalc -----------------------------------------------------------------------------------------------------
content("A grid of named rows and columns, 1978", STORY["BricklinVisiCalc1979"]["when"],
        [card("Dan Bricklin and Bob Frankston", "Bricklin pictured an electronic spreadsheet in the spring of 1978 as an MBA student "
              "at Harvard Business School. With Bob Frankston he made VisiCalc, which came out on the Apple II in 1979.",
              0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Spring 1978: the idea, at Harvard Business School",
             "8 Oct 1978: first prototype on an Apple II",
             "1979: VisiCalc, published by Personal Software",
             "Today: sheet['A1'] still names a cell by letter and row"]},
         factrow("BricklinVisiCalc1979")],
        story_notes("BricklinVisiCalc1979"),
        "The grid of named rows and columns is the idea openpyxl still addresses.")

# ---- 9 Project 9: program ----------------------------------------------------------------------------------------------------
a9, b9 = span("project9CensusTally_v1_0_0.py", "import openpyxl, pprint", "print('Done.')")
w1 = pw("project9CensusTally_v1_0_0.py", (a9, b9), False)
p1, bot = prog("project9CensusTally_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, lines=(a9, b9), show_out=False)
t1 = transcript("project9CensusTally_v1_0_0.py", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), fs=7.0, label="what the whole run printed")
content("Project 9: tally the census, county by county", "Open the sheet, loop over the rows, count tracts and add populations",
        [p1, t1,
         card("The result is a module", "The lines not shown import census2010, the file the program has just written, and print the "
              "Anchorage entry. pprint.pformat returns a dictionary as valid Python with its keys sorted.",
              round(0.5 + w1 + 0.15, 2), round(1.55 + t1["h"] + 0.15, 2), round(9.55 - (0.5 + w1 + 0.15), 2), round(4.95 - (1.55 + t1["h"] + 0.15), 2), fs=10)],
        "Project 9 reads a sheet of census data, one row for each census tract, and tallies tracts and population for each county "
        "in a dictionary of dictionaries: state to county to a dictionary with the keys tracts and pop. The listing is the "
        "chapter's three steps assembled, with the step markers removed. The typeset listing of Step 1 has call-out markers "
        "inside the code and raises SyntaxError at the marker as printed, and Step 2 compiles only when the marker is replaced by "
        "one space and not removed, which is why this run uses the repaired listing. The loop starts at row 2 to skip the header "
        "and reads columns B, C and D of each row. The excerpt is lines 15 to 33 of the 39 in the recording; the first 14 lines "
        "make the stand-in file, a short sheet with the columns of the real census file, and the last lines, not shown, import "
        "census2010 and print the Anchorage entry, then the file itself. A script's own folder is on sys.path, so the import "
        "finds the file the program wrote, and importing runs it. The run on the stand-in tallied three tracts and 12,515 people "
        "in Anchorage. Run whole on the real censuspopdata.xlsx of the book's online materials, 72,865 tract rows, the same "
        "program left {'pop': 291826, 'tracts': 55} for Anchorage. The shipped script readCensusExcel.py does not run today, as "
        "the previous slide on opening workbooks said, and the shipped census2010.py equals the generated file except that its "
        "line endings are Windows ones.",
        "Loop over the rows, tally in a dictionary, write the result as Python.")

# ---- 10 Project 9: diagram + table ---------------------------------------------------------------------------------------------
dg, dcap = diagram("ProjectNineTally", "activity", (0.5, 1.45, 5.9, 3.15),
                   grid={"open": (0, 0), "row": (0, 1), "has": (0, 2), "set": (1, 2), "add": (0, 3), "more": (0, 4),
                         "write": (1, 4), "imp": (1, 5)},
                   cols=[(0.3, 2.7), (3.55, 2.0), (5.6, 0.3)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 2, "row": 5},
                   routes={("start", "open"): "h", ("set", "add"): "vh", ("more", "row"): "loopL", ("imp", "end"): "h"}, fs=8, nh=0.46, dh=0.46)
trows = EX["_tables"]["countyTally"]["rows"]
tbl = {"t": "table", "x": 6.65, "y": 1.5, "w": 2.85, "colW": [0.55, 0.95, 0.5, 0.85], "fs": 8, "rowH": 0.27, "rows": trows}
content("Project 9 as a workflow", "One pass over the rows, one decision about the dictionary, one about the loop",
        [dg, dcap, tbl,
         card("One setdefault call", "It inserts a key only when the key is missing and always returns the value, so the loop can "
              "call it on every row. Without it the first row of a state raises KeyError.", 6.65, 3.25, 2.85, 1.7, fs=10, accent="slate")],
        "The program is drawn as an activity. It opens the workbook and gets the census sheet, then loops: it reads the state, "
        "county and population of the next row, and asks whether the state and the county exist in county_data yet. If not, "
        "setdefault adds the state, the county and the two counters; either way one tract and the tract's population are added to "
        "the county, and the loop goes on while a row is left up to max_row. When it ends, pprint.pformat writes the dictionary "
        "into census2010.py and import census2010 reads the result as a module. setdefault inserts a key with a default only "
        "when the key is missing and always returns the value, so one call on every row is enough; without it the first row of a "
        "state raises KeyError. The table is the dictionary the program wrote on the stand-in sheet, one row for each county, "
        "computed again from the stand-in sheet by the deck's check. Two cautions from the research belong here. The bounds of "
        "the loop are the sheet's size, so a sheet with touched empty rows runs the loop over rows that hold no data and int(None) "
        "raises TypeError, as the previous slide showed. And the result file is Python source that is run when imported, so "
        "ast.literal_eval is the safer way to read a dictionary written by someone else.",
        "Read a row, make sure the keys exist, add, and repeat to max_row.")

# ---- 11 writing ------------------------------------------------------------------------------------------------------------
a11, b11 = span("writingWorkbooks_v1_0_0.py", "import openpyxl", "print(sheet['A1'].value)")
w1 = pw("writingWorkbooks_v1_0_0.py", (a11, b11), False)
p1, bot = prog("writingWorkbooks_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, lines=(a11, b11), show_out=False)
t1 = transcript("writingWorkbooks_v1_0_0.py", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), fs=7.0, label="what the whole run printed")
content("Writing workbooks and saving them", "A new Workbook starts with one sheet called Sheet; save() writes the file",
        [p1, t1,
         card("Titles are checked, files are not", "Sheet titles stay unique without regard to case, and a slash is refused with "
              "ValueError. save() replaces an existing file without a question.",
              round(0.5 + w1 + 0.15, 2), round(1.55 + t1["h"] + 0.15, 2), round(9.55 - (0.5 + w1 + 0.15), 2), round(4.95 - (1.55 + t1["h"] + 0.15), 2), fs=10, accent="slate")],
        "Writing starts from openpyxl.Workbook(), which holds one sheet named Sheet; wb.active is that sheet, and assigning to its "
        "title attribute renames it. save() writes the workbook to the file name it is given, and when that name exists the old "
        "file is replaced without a question, which is why the chapter's projects save under a new name. create_sheet adds a "
        "sheet named SheetN at the end, or at an index with a title, and returns the new Worksheet, so print shows it; the del "
        "operator removes a sheet by its name like a key from a dictionary, and assigning to a cell's value writes it. The excerpt "
        "is lines 14 to 33 of the 35 in the recording. The last two lines of the program, not shown, create three sheets with "
        "the titles Dup, Dup and dup and print Dup Dup1 dup2, the last line of the transcript: titles are kept unique without "
        "regard to case by adding a number. A title with a slash, a bracket, a star or a question mark is refused with ValueError, "
        "and a title longer than 31 characters, the limit of Excel, only draws a warning. The excerpt's sheet names also show "
        "what the chapter's session shows, ['First Sheet', 'Sheet', 'Middle Sheet', 'Sheet1'] before the two deletions and "
        "['First Sheet', 'Sheet'] after them.",
        "Workbook() makes a file in memory; nothing exists on disk until save().")

# ---- 12 Project 10: program -----------------------------------------------------------------------------------------------------
a12, b12 = span("project10UpdateProduce_v1_0_0.py", "import openpyxl", "wb.save('updatedProduceSales3.xlsx')")
w1 = pw("project10UpdateProduce_v1_0_0.py", (a12, b12), False)
p1, bot = prog("project10UpdateProduce_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, lines=(a12, b12), show_out=False)
t1 = transcript("project10UpdateProduce_v1_0_0.py", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), fs=7.0, label="what the whole run printed")
content("Project 10: correct the prices, keep the original", "A dictionary holds the corrections; the loop writes column 2; save() uses a new name",
        [p1, t1,
         card("Row 2 to max_row", "range(2, sheet.max_row + 1) skips the header and reaches the last row; "
              "with range(2, sheet.max_row) the last row would be left out.", 0.5, round(bot + 0.12, 2), w1, round(4.95 - bot - 0.12, 2), fs=10.5),
         card("The last line", "Each line not shown prints old price, new price and formula. The final None is D2 of the saved copy read with data_only=True.",
              t1["x"], round(t1["y"] + t1["h"] + 0.12, 2), t1["w"], round(4.95 - t1["y"] - t1["h"] - 0.12, 2), fs=10, accent="slate")],
        "Project 10 corrects the price of three kinds of produce in a spreadsheet of sales. The corrections are in a dictionary at "
        "the top of the program, so the loop needs one if statement and a new correction changes data and not code. The loop "
        "starts at row 2 to skip the header, reads column 1 with cell() and writes column 2 only for names in the dictionary, "
        "and the workbook is saved as updatedProduceSales3.xlsx so that the original is not overwritten. The excerpt is lines 15 "
        "to 29 of the 33 in the recording; lines 30 and 31 compare the old and new sheets row by row, and line 33 reads D2 of the "
        "saved copy. The transcript shows the corrections applied: Garlic 1.19 became 3.07 in rows 3, 7 and 11, Celery 3.07 became "
        "1.19 and Lemon 1.29 became 1.27, while the formula in column D is unchanged. Run whole on the real produce file, the same "
        "program changed Garlic in 630 rows, Celery in 586 and Lemon in 607. The script updateProduce.py that ships with the book "
        "does not run today: it opens a file named produceSales.xlsx that is not in the zip, the file being produceSales3.xlsx, and "
        "its loop range(2, get_highest_row()) calls a method that no longer exists and would leave the last row out.",
        "Corrections live in a dictionary; the loop applies them and saves a copy.")

# ---- 13 Project 10: diagram ---------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ProjectTenUpdate", "activity", (0.5, 1.45, 6.0, 3.15),
                   grid={"dict": (0, 0), "open": (0, 1), "name": (0, 2), "key": (0, 3), "write": (1, 3), "more": (0, 4),
                         "save": (0, 5), "lost": (1, 5)},
                   cols=[(0.3, 2.75), (3.7, 2.0), (5.7, 0.3)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 2, "row": 5},
                   routes={("start", "dict"): "h", ("write", "more"): "vh", ("more", "name"): "loopL", ("lost", "end"): "h"}, fs=8, nh=0.46, dh=0.46)
content("Project 10 as a workflow, and what it loses", "The last box is the one the chapter does not draw: the results Excel stored are gone",
        [dg, dcap,
         card("Saved totals: gone", "openpyxl keeps the formulas but not the results Excel stored. On the real produce file "
              "D2 held 18.58 in the original and None in the copy.", 6.7, 1.5, 2.8, 1.65, fs=10),
         card("Office app restores", "Run headless on the saved file, LibreOffice 24.2.7.2 recalculated all 23,757 "
              "rows with 0 differences from the totals Excel had stored.", 6.7, 3.3, 2.8, 1.65, fs=10, accent="slate")],
        "This is the workflow of the project, and its last two boxes are the finding. The loop reads the produce name of each row "
        "from row 2, asks whether it is a key of PRICE_UPDATES, writes the new price in column 2 if so, and goes on while a row is "
        "left up to max_row + 1; then the workbook is saved under the new name. The saved formulas hold no stored results: a "
        "workbook that openpyxl saved keeps the formulas but not the results Excel had stored for them, so every TOTAL cell reads "
        "as None after Project 10 saves its copy, until a spreadsheet program opens and saves the copy again. On the real produce "
        "file D2 held 18.58 in the original and None in the copy. The chapter's remedy is to open the copy in Excel; LibreOffice "
        "24.2.7.2, run headless on the saved file, recalculated all 23,757 rows with 0 differences from the totals Excel had "
        "stored, so the step is a calculation any spreadsheet program can do and not something Python can do with openpyxl alone. "
        "The same loss happens to a chart or a picture only when the library cannot read it, which is not the case for a chart "
        "openpyxl wrote itself, as the chart slides show.",
        "Saving through openpyxl drops the stored results of every formula.")

# ---- 14 formulas program -------------------------------------------------------------------------------------------------------------
a14, b14 = span("formulasAndResults_v1_0_0.py", "import openpyxl, io, zipfile", "print(wb_data_only")
w1 = pw("formulasAndResults_v1_0_0.py", (a14, b14), False, 7.5)
p1, bot = prog("formulasAndResults_v1_0_0.py", 0.5, 1.55, w1, fs=7.5, lines=(a14, b14), show_out=False)
t1 = transcript("formulasAndResults_v1_0_0.py", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), fs=7.5, label="what the whole run printed")
content("Formulas: text that begins with an equal sign", "openpyxl stores the text, marks the cell f, and never calculates it",
        [p1, t1,
         card("Lines 26 to 37 play Excel's part", "They put the result 500 into the file's XML as a spreadsheet program does, so "
              "data_only=True reads 500. Loading and saving with openpyxl keeps the formula and drops the 500 ('=SUM(A1:A2) None'). "
              "The last line: =NOSUCHFUNC(1 is accepted unchecked.",
              0.5, round(bot + 0.12, 2), w1, round(4.95 - bot - 0.12, 2), fs=9.5)],
        "A formula is stored by assigning text that begins with an equal sign. openpyxl marks the cell as data type f, does not "
        "evaluate it and does not check that the function exists, so '=NOSUCHFUNC(1' is stored as it is typed. Loaded as usual, a "
        "formula cell gives back its formula text; loaded with data_only=True the same cell gives the value a spreadsheet program "
        "stored, or None when none did. In the transcript the first three lines are the type and text of A3, the formula read "
        "back, and the None that data_only=True gives for a file nobody has calculated. The excerpt is lines 14 to 25 of the 37 in "
        "the recording. The remaining lines make a copy of the saved file in which the result 500 has been put into the XML of A3, "
        "as Excel or LibreOffice would store it, and the transcript shows what follows: data_only=True now reads 500, and after "
        "openpyxl loads and saves that file again the formula is still there and the stored result is gone. That is the same loss "
        "as the totals of Project 10. The chapter says the file must be opened and saved in Excel for the result to be stored, and "
        "the research confirmed that this is the calculation; a program cannot take its place with openpyxl alone. The two "
        "details that matter most to a student are that a formula is text, so a typing mistake in it is not found until a "
        "spreadsheet program opens the file, and that data_only chooses between the formula and the stored value but never "
        "calculates.",
        "A formula is text; data_only=True reads what a spreadsheet program stored.")

# ---- 15 formula sequence ----------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AFormulaResult", "sequence", (0.5, 1.45, 9.0, 2.85), fs=9, head_w=1.9)
content("Who calculates a formula?", "The program writes it; Excel or LibreOffice calculates it; the program reads the result",
        [dg, dcap,
         {"t": "boxes", "x": 0.5, "y": 4.5, "w": 9.0, "h": 0.5, "cols": 3, "fs": 10.5, "subfs": 8.5, "accent": [0],
          "items": [{"label": "data_only=True", "sub": "reads a stored result, never calculates"},
                    {"label": "XlsxWriter stores 0", "sub": "unless it is given another result"},
                    {"label": "Spreadsheet program", "sub": "stores the result when it saves"}]}],
        "The exchange between the program and a spreadsheet application is drawn as a sequence because the order matters. The "
        "program assigns '=SUM(A1:A2)' to A3 and saves the file. The file is then opened and saved by the application, which "
        "calculates the formula and stores the result 500, and the saved file holds the formula and its result. Only then does "
        "load_workbook() without data_only read the formula and data_only=True read the stored result, 500. data_only=True "
        "chooses between the formula and the value stored at the last save by a spreadsheet program; it never calculates, so a "
        "file whose formulas were never calculated gives None for every formula cell. The library XlsxWriter, which writes "
        "formulas, stores the value 0 as the result unless it is given another, and sets a flag that makes the application "
        "recalculate on opening, so data_only=True reads 0 from a file that never held a calculated total. The step of opening "
        "and saving the file in Excel is therefore the calculation, and a recalculation is the job of a spreadsheet program: "
        "the next slide runs LibreOffice for it.",
        "Write the formula with Python; let a spreadsheet program calculate it.")

# ---- 16 recalc ------------------------------------------------------------------------------------------------------------------------------
a16, b16 = span("recalcWithLibreOffice_v1_0_0.py", "print('exit', r.returncode)")
w1 = pw("recalcWithLibreOffice_v1_0_0.py", (a16, b16), True)
p1, bot = prog("recalcWithLibreOffice_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, lines=(a16, b16), show_out=True)
content("Who calculates? A spreadsheet program", "LibreOffice, run headless, stores the results; ROUND and round() disagree on exact halves",
        [p1,
         card("Line 20 runs soffice", "soffice --headless --convert-to xlsx --outdir out produceSales3.xlsx opens and saves the "
              "stand-in produce file, so its TOTAL cells get stored results again. D3 now reads 11.9.",
              0.5, round(bot + 0.12, 2), w1, round(4.95 - bot - 0.12, 2), fs=9.5, accent="slate"),
         card("ROUND, not round()", "On the real produce file Excel's stored =ROUND(B*C,2) differed from Python's "
              "round(price * pounds, 2) in 629 of 23,757 rows. 1.89 * 34.5 is held a hair under 65.205.",
              round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), 3.4, fs=10.5)],
        "A spreadsheet program does the calculating, and LibreOffice can be driven without a window. The program checks that "
        "soffice is on the machine, then, in the line the excerpt does not show, runs it headless with --convert-to xlsx, which "
        "opens the stand-in produce file and saves it again, so that every TOTAL cell gets a stored result. It then compares "
        "those stored totals with Python's round(b * c, 2) and prints how many differ: 4 of the 10 rows of the stand-in. The "
        "reason is that a spreadsheet's ROUND and Python's round can disagree on an exact half: Python rounds the binary number "
        "its float holds, and 1.89 times 34.5 is held a little under the exact half 65.205, so Python gives 65.2 where Excel "
        "stores 65.21. On the real produce file Excel's stored total differed from Python's in 629 of 23,757 rows, and "
        "LibreOffice's recalculation of the updated file in 695. A program that checks a total therefore has to allow the "
        "difference or use the decimal module. The last line of the transcript shows that LibreOffice stored 11.9 for D3 and that "
        "the formula text is unchanged. LibreOffice 24.2.7.2 and the stand-in file were used here; Microsoft Excel itself was not "
        "available.",
        "Recalculate with a spreadsheet program, and expect ROUND to differ from round().")

# ---- 17 story: Herndon ------------------------------------------------------------------------------------------------------------------------------
content("A spreadsheet error that left five countries out", STORY["HerndonSpreadsheet2013"]["when"],
        [card("Herndon, Ash and Pollin", "In April 2013 their working paper replicated Reinhart and Rogoff's study of public debt "
              "and growth. A spreadsheet coding error had excluded five countries from the analysis.",
              0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Apr 2013: the working paper is published",
             "Left out: Australia, Austria, Belgium, Canada, Denmark",
             "Growth above 90% debt: 2.2% a year, not -0.1%",
             "A formula is code: give it a second reader"]},
         factrow("HerndonSpreadsheet2013")],
        story_notes("HerndonSpreadsheet2013"),
        "A spreadsheet formula is code, so it needs a second reader and a test.")

# ---- 18 fonts and sizes -------------------------------------------------------------------------------------------------------------------------------------
w1 = pw("fontsAndSizes_v1_0_0.py", None, False, 7.0)
p1, bot = prog("fontsAndSizes_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, show_out=False)
t1 = transcript("fontsAndSizes_v1_0_0.py", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), fs=7.0, label="what the run printed")
content("Fonts, row heights and column widths", "A Font is an object you assign; sizes live in row_dimensions and column_dimensions",
        [p1, t1,
         card("A Font keeps only what it is given", "Font(size=24, italic=True) writes no name, and the book's Calibri 11 holds only "
              "for cells never styled. A style cannot be changed in place; assign a new Font.",
              round(0.5 + w1 + 0.15, 2), round(1.55 + t1["h"] + 0.15, 2), round(9.55 - (0.5 + w1 + 0.15), 2), round(4.95 - (1.55 + t1["h"] + 0.15), 2), fs=10)],
        "A Font object holds styling, is made with keyword arguments and is assigned to a cell's font attribute; a value assigned "
        "to the cell afterwards keeps the font. Table 14-2 of the chapter lists name, size, bold and italic. The research found "
        "that the defaults the chapter states are only half true. A Font made without a name or size writes neither into the "
        "file, so Font(size=24, italic=True) has no name and Font(name='Times New Roman', bold=True) has no size, as the first "
        "two lines of the transcript show, while the untouched cell C5 reads Calibri 11. A cell with such a font is drawn in "
        "whatever the application chooses; LibreOffice 24.2 drew the cell with no name in Caladea, a substitute for Cambria, and "
        "Excel itself was not available to say what it draws. Style objects are shared between cells and cannot be changed in "
        "place: assigning cell.font.bold raises AttributeError, so the style must be replaced by a new Font. Row heights and "
        "column widths are set through row_dimensions and column_dimensions, a row addressed by its number and a column by its "
        "letter. The hidden attribute hides a column, which the chapter's Practice Question 16 asks for and the chapter never "
        "shows, and the file records hidden=1 in the transcript's second col element. Reading a dimension creates it: looking at "
        "row_dimensions[3].height adds a row that is saved as an empty row element, and looking at column_dimensions['A'].width "
        "adds a column entry saved with a custom width of 13. This program is the font, size and hide lines of the corpus program "
        "layoutFontMergeFreeze, with the prints cut to lines that fit the slide.",
        "A style is a new object; a size lives in the sheet's dimensions.")

# ---- 19 merge and freeze ------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AMergedRange", "states", (0.5, 1.45, 4.5, 2.6), fs=8, sw=1.4, sh=1.05, sfs=8.5, stepy=0.5)
w1 = pw("mergeAndFreeze_v1_0_0.py", None, True, 7.0)
p1, bot = prog("mergeAndFreeze_v1_0_0.py", round(9.55 - w1, 2), 1.55, w1, fs=7.0, show_out=True)
content("Merge cells and freeze panes", "A merged range keeps one real cell; a frozen pane keeps the rows above and columns left",
        [dg, dcap, p1,
         {"t": "foot", "x": 0.5, "y": round(dcap["y"] + dcap["h"] + 0.06, 2), "w": 4.5, "h": 0.4, "fs": 9.5,
          "body": "freeze_panes = 'A2' freezes row 1, 'B1' column A, 'C2' row 1 and columns A, B. It does not move the view."}],
        "Merging joins a rectangle of cells into one. After merge_cells('F1:I3') only F1 is a real Cell; the others are MergedCell "
        "objects whose value is read-only, so assigning to G2 raises AttributeError, and the values the other cells held are "
        "discarded at once. unmerge_cells gives back empty separate cells with the text in the top-left one, the last two lines "
        "of the transcript before the freeze settings. The state diagram follows one rectangle: merge_cells takes it from "
        "individual cells to one merged cell with the value of the top-left cell, unmerge_cells takes it back, and assigning to a "
        "MergedCell is the loop that raises an error. Freezing panes freezes the rows above and the columns left of the named "
        "cell, not that cell's own row and column: A2 freezes row 1, B1 column A, C1 columns A and B, and C2 row 1 with columns A "
        "and B, which the xSplit and ySplit values in the transcript show. Setting freeze_panes to None or to A1 removes them. "
        "Freezing does not move the view: the book's produceSales3.xlsx was saved scrolled to row 23736 and a copy frozen at A2 "
        "still opened at that row, so the frozen copy of Figure 14-8 shows the bottom of the data unless the program also resets "
        "the view. This program is the merge and freeze lines of the corpus program layoutFontMergeFreeze, with its prints cut "
        "to lines that fit the slide.",
        "A merged range keeps one real cell; freeze_panes freezes above and left.")

# ---- 20 charts program ---------------------------------------------------------------------------------------------------------------------------------------------------
a20, b20 = span("barChart_v1_0_0.py", "for i in range(1, 11)", "wb.save('sampleChart3.xlsx')")
a20 -= 3
w1 = pw("barChart_v1_0_0.py", (a20, b20), False)
p1, bot = prog("barChart_v1_0_0.py", 0.5, 1.55, w1, fs=7.0, lines=(a20, b20), show_out=False)
t1 = transcript("barChart_v1_0_0.py", 0.5, round(bot + 0.34, 2), tw("barChart_v1_0_0.py"), fs=7.0, label="what the whole run printed")
content("Charts: Reference, Series, BarChart", "A chart is built from a rectangle of cells and anchored to a cell",
        [p1, t1,
         card("Column first", "Reference(sheet, 2, 1, 2, 10) is B1:B10. The signature is min_col, min_row, max_col, max_row; the "
              "chapter's sentence that the row comes first has it backwards.", round(0.5 + w1 + 0.15, 2), 1.55, round(9.55 - (0.5 + w1 + 0.15), 2), 3.4, fs=10.5)],
        "Four things make a chart in openpyxl: a Reference names a rectangle of cells, Series builds a series from the reference with "
        "a title given as text, a chart object such as BarChart is made empty and given a title, and the series is added with "
        "append; add_chart anchors the chart to the cell named in its second argument. The excerpt is lines 14 to 26 of the 32 in "
        "the recording. The transcript's first line is the Reference, 'Sheet'!$A$1:$A$10. The chapter states the order of the "
        "arguments the wrong way round: it says the row comes first, whereas the signature of openpyxl 3.1.5 is Reference(worksheet, "
        "min_col, min_row, max_col, max_row), column first, and Reference(sheet, 2, 1, 2, 10) is B1:B10. The chapter's example hides "
        "the mistake because it is a square block of cells, and leaving max_row out silently gives a single cell, the last "
        "reference printed. The second line lists the three parts of the zip that a chart adds, xl/charts/chart1.xml and the "
        "drawing that anchors it. The two 1s are the numbers of charts found after loading the saved file and after loading a "
        "file saved again: a chart that openpyxl wrote survives a load and a save. The chapter's use of openpyxl.chart after "
        "import openpyxl alone works in 3.1.5, so the call is correct as printed.",
        "A Reference is column first: min_col, min_row, max_col, max_row.")

# ---- 21 chart diagram + native chart ---------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ABarChartInFiveSteps", "activity", (0.5, 1.45, 5.2, 3.15),
                   grid={"ref": (0, 0), "series": (0, 1), "chart": (0, 2), "append": (0, 3), "add": (0, 4), "save": (0, 5)},
                   cols=[(0.0, 4.5), (4.75, 0.4)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "ref"): "h", ("save", "end"): "h"}, fs=8.5, nh=0.46, dh=0.46)
ch = EX["_charts"]["squares"]
chart = {"t": "chart", "ctype": "bar", "x": 5.9, "y": 1.45, "w": 3.6, "h": 2.05, "labels": ch["labels"], "title": "Cells A1 to A10: the squares",
         "series": [{"name": "First series", "data": ch["values"]}], "dataLabels": True, "dlFs": 8}
content("A bar chart in five steps", "The five steps of the chapter, then the ten cells they chart, drawn here as a native chart",
        [dg, dcap, chart,
         card("Saved as XML", "Saved as xl/charts/chart1.xml with a drawing part that anchors it. C5 is column index 2 and "
              "row index 4: the file counts from zero.", 5.9, 3.6, 3.6, 1.35, fs=9.5, accent="slate")],
        "This is the chapter's own list of five steps, each depending on the one before it, with no choice on the way, so it is "
        "drawn as a workflow. A Reference names a rectangle of cells from min_col, min_row, max_col and max_row; Series(ref_obj, "
        "title='First series') builds a series from it; BarChart() creates the chart object and its title is set; "
        "chart_obj.append(series_obj) adds the series; and sheet.add_chart(chart_obj, 'C5') adds the chart to the sheet at a cell. "
        "save() then writes the chart into xl/charts/chart1.xml. The chapter names four chart classes, BarChart, LineChart, "
        "ScatterChart and PieChart, and each is written into the file as a chart element of its own kind; a scatter chart needs "
        "the x values too, passed as xvalues. The native chart on the right is not the chart Excel will draw. It is a PowerPoint "
        "chart of the ten cells the Reference names, A1 to A10, which hold the squares 1 to 100, and the deck check reads those "
        "cells from the saved workbook again and compares them with the chart. How the real chart looks is decided by the "
        "application that opens the file: LibreOffice 24.2 drew the chapter's chart with a value axis from 0 to 120, the labels 1 "
        "to 10 and the legend First series, and Excel was not available to compare. copy_worksheet copies cells and leaves charts "
        "behind, contrary to the warning in the documentation that shapes are lost.",
        "Five steps: Reference, Series, chart, append, add_chart.")

# ---- 22 practice programs ---------------------------------------------------------------------------------------------------------------------------------------------------------
am, bm = span("multiplicationTable_v1_0_0.py", "for i in range(1, n + 1):", "sheet.cell(row=i + 1, column=j + 1")
wm = pw("multiplicationTable_v1_0_0.py", (am, bm), True)
p1, bot1 = prog("multiplicationTable_v1_0_0.py", 0.5, 1.55, wm, fs=7.0, lines=(am, bm), show_out=True)
ab, bb = span("blankRowInserter_v1_0_0.py", "sheet.insert_rows(n, m)", "print([out.cell")
wb_ = pw("blankRowInserter_v1_0_0.py", (ab, bb), True)
p2, bot2 = prog("blankRowInserter_v1_0_0.py", 0.5, round(bot1 + 0.4, 2), wb_, fs=7.0, lines=(ab, bb), show_out=True)
content("Practice programs: a table and blank rows", "A multiplication table, and blank rows inserted into a sheet",
        [p1, p2,
         card("Labels in bold", "Row 1 from B1 and column A from A2 hold the labels 1 to 6, products fill B2 to G7; the table spans A1:G7.",
              round(0.5 + wm + 0.15, 2), 1.55, round(9.55 - (0.5 + wm + 0.15), 2), round(bot1 - 1.55, 2), fs=9, accent="slate"),
         card("Formulas stay", "The SUM stayed over B1:B5, merged ranges stayed, and row heights stayed.",
              round(0.5 + wb_ + 0.15, 2), round(bot1 + 0.4, 2), round(9.55 - (0.5 + wb_ + 0.15), 2), round(bot2 - bot1 - 0.4, 2), fs=9)],
        "The chapter's two practice programs take their numbers from sys.argv, a list of strings with the script name first, so int() "
        "converts them and a missing argument raises IndexError; here the first line sets sys.argv instead of the command line. "
        "Multiplication Table Maker puts the labels 1 to N in bold along row 1 from B1 and down column A from A2, with the products "
        "inside, so the table for 6 spans A1 to G7, D5 is 12, G7 is 36 and A1 is empty. Blank Row Inserter reads N, M and a file name "
        "and makes one call, insert_rows(idx, amount), which inserts blank rows before row idx and moves the cells below it down "
        "with their values and styles. That is correct for values and incomplete for everything else, and the chapter says nothing "
        "of it. insert_rows does not rewrite the references inside formulas: the SUM over B1:B5 stays over B1:B5, as the printed "
        "'=SUM(B1:B5)' at C8 shows, and C6 is now empty. It does not move merged ranges, and it does not move row heights: a height "
        "of 50 set on row 4 stayed on row 4 after two rows were inserted at row 3. The program must fix the rest itself, or the "
        "formulas will add the wrong cells. Four further notes on the chapter's practice questions: Question 10 asks for the string "
        "name of row 14, which does not exist because rows have numbers and only columns have letters; Question 11 has "
        "sheet['A1':'F1'] return a tuple of one tuple; Question 16 asks how to hide a column, which the chapter never shows; and "
        "Question 18 lists Reference, Series, BarChart, append and add_chart.",
        "insert_rows moves values and styles; formulas, merges and heights stay put.")

# ---- 23 files you did not make -------------------------------------------------------------------------------------------------------------------------------------------------------
pl, botl = prog("liveExample3_v1_0_0.py", 0.5, 1.55, pw("liveExample3_v1_0_0.py", None, True, 7.0), fs=7.0, show_out=True)
ts = transcript("safeLoadEntityBomb_v1_0_0.py", 0.5, round(botl + 0.42, 2), tw("safeLoadEntityBomb_v1_0_0.py"), fs=7.0,
                label="transcript of program safeLoadEntityBomb_v1_0_0.py: needs defusedxml")
wl = pw("liveExample3_v1_0_0.py", None, True, 7.0)
content("Files you did not make", "Download example3.xlsx from the book's site; load a zip bomb safely",
        [pl, ts,
         card("Live download", "requests.get fetched example3.xlsx and openpyxl read it from memory. The "
              "transcript is LIVE: it is what the book's site answered on 12 October 2026.",
              round(0.5 + wl + 0.15, 2), 1.55, round(9.55 - (0.5 + wl + 0.15), 2), round(botl - 1.55, 2), fs=9.5),
         {"t": "foot", "x": 0.5, "y": round(ts["y"] + ts["h"] + 0.06, 2), "w": 9.0, "h": round(4.95 - (ts["y"] + ts["h"] + 0.06), 2), "fs": 9,
          "body": "Ten nested entities of ten copies each fit in under 6000 bytes. With defusedxml installed, load_workbook refused both files with ValueError."}],
        "An .xlsx file is a zip of XML parts that openpyxl parses without guarding against entity attacks, and the chapter opens "
        "files it did not make. The first program is the only one in this deck that reaches the real web: it downloads "
        "example3.xlsx from automatetheboringstuff.com, 9,904 bytes with status 200, loads it from memory with io.BytesIO and "
        "prints its three sheets, its size of 7 rows by 3 columns and the first three rows, the first of them 'Apples', 73 with "
        "the datetime of 5 April 2035. The second transcript is the safe-loading program. It builds a workbook whose sheet has a "
        "nested entity, ten copies of ten copies and so on, in a file under six kilobytes, and loads it with openpyxl. The page of "
        "the openpyxl documentation says openpyxl does not guard against quadratic blowup or billion laughs and advises installing "
        "defusedxml. Run on Python 3.14.6, whose bundled Expat is 2.8.1, a nested entity of depth 4 loaded into 100,000 characters "
        "in a cell without defusedxml and a depth of 6, ten million characters, was refused by Expat with a limit on input "
        "amplification; with defusedxml installed, as in this transcript, load_workbook refused both with ValueError. The Python "
        "documentation says Expat versions below 2.7.2 may still be vulnerable, so the protection depends on the library the "
        "interpreter was built with. The program names defusedxml, so it is run with that package added to the interpreter, the "
        "only package besides openpyxl and requests.",
        "Treat a workbook you did not make as untrusted input: install defusedxml.")

# ---- 24 summary: the mind map -------------------------------------------------------------------------------------------
dg, dcap = diagram("ExcelSpreadsheetsAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.35), fs=9, root_w=1.5)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. Workbooks and sheets come first: load_workbook() returns a Workbook object, the "
        "active sheet is the one on top, and create_sheet() and del add and remove sheets. Cells and ranges follow: a cell is got "
        "by its name or by row and column numbers, max_row and max_column give the size of the sheet, and a slice of two cell "
        "names gives a tuple of rows. The projects put these together: Project 9 tallies tracts and population by county, "
        "Project 10 corrects prices in the produce sheet, and the practice programs make a table and insert rows. Formulas are "
        "text that begins with an equal sign, openpyxl does not calculate them, and data_only=True reads the stored result. "
        "Formatting is Font() for the name, size, bold and italic, row heights and column widths through dimensions, and "
        "merge_cells() and freeze_panes for how cells show. Charts are a Reference that names a rectangle of cells, a Series "
        "appended to a chart object, and add_chart() anchoring the chart to a cell. Together they answer the first question of "
        "the chapter, which object keeps what, and the slides that say where a printed line differs answer the second.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 14 - free online", PUB["P01"][2]],
         ["openpyxl documentation", PUB["P02"][2]],
         ["openpyxl tutorial", PUB["P03"][2]]]
_ref = [["Worksheet API: merge, freeze, insert", PUB["P04"][2]],
        ["Working with styles", PUB["P05"][2]],
        ["Charts: introduction", PUB["P06"][2]],
        ["Chart Reference arguments", PUB["P08"][2]]]
_hist = [["VisiCalc: Bricklin's idea, 1978", STORY["BricklinVisiCalc1979"]["link"]],
         ["Microsoft Excel (Wikipedia)", STORY["MicrosoftExcel1985"]["link"]],
         ["Office Open XML (Library of Congress)", STORY["OoxmlStandard2006"]["link"]],
         ["openpyxl, by Gazoni and Clark", STORY["OpenpyxlLibrary2010"]["link"]],
         ["Gene name errors (Genome Biology)", STORY["ZiemannGeneNames2016"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The "
        "textbook chapter is free to read online and holds every listing of the chapter, the openpyxl documentation and tutorial "
        "cover what this deck added to the chapter, and the reference links are the official pages for the worksheet methods, the "
        "styles and the charts, including the arguments of Reference. The history links are the sources behind five of the six "
        "stories of the chapter. Two of them are slides: the grid of named rows and columns of Bricklin's idea and the "
        "standardisation of the Office Open XML format. The other three were told in the notes: the birth of openpyxl in 2010 on "
        "the library slide, Excel and its 1900 leap-year bug in 1985 and the gene symbols that Excel turns into dates in 2016 on "
        "the slide about cells. The sixth story, the Herndon, Ash and Pollin paper, has its source link on its own slide, because "
        "the address is too long for this list.",
        "Textbook, documentation and history, opened the day this deck was built.")

# ---- 26 closing -----------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "I open a workbook, pick a sheet by name and a cell by name or by two numbers.",
            "openpyxl stores formulas and loses their stored results: a spreadsheet program calculates.",
            "I look before I loop, because a touched cell enlarges the sheet.",
            "I save under a new name, and I treat a file I did not make as untrusted."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for k, v in G.items()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples "
        "yourself, you have the chapter. The next chapter of the book works with Google Sheets, where a program reaches a "
        "spreadsheet through a web service instead of a file, and everything this chapter taught about sheets, cells and "
        "formulas carries over to it.",
        "Questions are welcome; bring a workbook to read.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Files, sheets and cells", "openpyxl and the .xlsx file", "A grid of named rows and columns, 1978"),
          ("Project 9: reading data", "Project 9: tally the census, county by county", "Project 9 as a workflow"),
          ("Writing workbooks and Project 10", "Writing workbooks and saving them", "Project 10 as a workflow, and what it loses"),
          ("Formulas and who calculates", "Formulas: text that begins with an equal sign", "A spreadsheet error that left five countries out"),
          ("Formatting cells", "Fonts, row heights and column widths", "Merge cells and freeze panes"),
          ("Charts", "Charts: Reference, Series, BarChart", "A bar chart in five steps"),
          ("Practice programs and untrusted files", "Practice programs: a table and blank rows", "Files you did not make"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + 3" % _nstory, "label": "true stories: %d on slides, 3 in the notes" % _nstory},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Eight parts; every range is a run of slides you can jump to"
S[1]["take"] = "Eight parts, from a file to a chart."
S[1]["notes"] = ("The route has eight parts. It starts with files, sheets and cells, the openpyxl library and the way a workbook is "
                 "opened and a cell is named, then Project 9, which reads a census sheet and tallies it by county, then writing "
                 "workbooks and Project 10, which corrects prices and saves a copy, then formulas and the question of who "
                 "calculates them, then formatting with fonts, sizes, merged cells and frozen panes, then charts, then the "
                 "chapter's practice programs and the safe way to open a file one did not make, ending with a one-map summary "
                 "and the resources. The ranges name the exact slides, so you can return to the part you need. Three of the "
                 "slides are true stories that explain where a tool or an idea of this chapter came from, and three more are "
                 "told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as the "
                 "interactive page.")

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
plan = {"meta": {"title": "Chapter 14: Excel Spreadsheets", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])))
