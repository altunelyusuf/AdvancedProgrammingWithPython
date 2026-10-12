#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 18 (CSV, JSON, and XML Files) on the CME classroom standard.

Same regime as chapters 10 to 17: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources,
full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their
line numbers) with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with xmltodict 1.0.4 and defusedxml 0.7.1; csv, json and
xml.etree.ElementTree are the standard library); the speaker notes are prose for the reader and carry only what the chapter's RDODI
research package (03-materials/ch18/rdodi, sen0414_ch18_rdodi_data_v1_0_2.py, findings F1 to F18), its records
(08-tooling/ch18-page/*.json) or a program of this deck established.

What this chapter adds against chapter 17: the programs need no package beyond the standard library except the two that the XML slides
name (xmltodict and defusedxml), and every file they work on is made by the programs themselves in a temporary folder, so no program is
LIVE and none needs the network. What could not be run is marked NOT EXECUTED on its slide: Microsoft Excel and a real Windows computer
(slide 10) and the final Python 3.15 release and Python 3.14.7 and later (slide 13); the effect of Windows on line ends is shown by
an emulation (an io.TextIOWrapper asked for the translation Windows does) and the slide says EMULATED, as honesty_check_v1_0_0.py
requires. The measured numbers of the research (memory of a 300,000-row file, the Excel-to-CSV converter) are marked 'single run' on
their slides. The eight narrative diagrams of the chapter (sen0414_ch18_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native
shapes (diagram_shapes_v1_0_0.py, with a column-of-states diagram that has a skipping arrow added for a value through JSON) and checked
by diagram_check_v1_0_0.py; two tables (the quoting constants, the texts json.loads refuses) and one chart (the size of one person in
JSON and XML) are native PowerPoint objects whose data the deck check computes again; no photograph is used, because the research could
not fetch and licence one (Wikimedia Commons answered 429); two of the six stories are slides (CSV in 1972, the first JSON message) and
four are told in the notes.

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


ST = load("stories18", os.path.join(HERE, "..", "sen0414_ch18_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams18", os.path.join(HERE, "..", "sen0414_ch18_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi18", os.path.join(HERE, "..", "sen0414_ch18_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s, %s" % (PYV, EX["_packages"].split(" | ")[0] + ", " + EX["_packages"].split(" | ")[1])
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires 'EMULATED' on every slide that shows an emulation, 'single run' on every slide that
# shows a measured time and 'NOT EXECUTED' on every slide the plan lists, and on no other)
L_NOTEXEC = "NOT EXECUTED"
L_ONCE = "single run"
L_EMU = "EMULATED"


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
    L = pr["code"].rstrip("\n").split("\n")
    a, b = lines
    n = (b - a + 1) + (pr["transcript"].count("\n") + 1 if out and pr["transcript"] else 0)
    fs = hi
    while fs >= lo:
        if pw(pname, lines, out, fs) <= wmax and n * (fs * 1.22 / 72.0 + 0.02) + 0.30 <= hmax:
            return fs
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d do not fit %.2f x %.2f in at %.1f pt" % (pname, a, b, wmax, hmax, lo))


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
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: caption %r is too long for a %.2f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, fs=7.0, label=None, aligned=False):
    """The transcript of a program in a panel of its own. With a label of the form 'transcript of program <name>' the panel is
    re-run by program_check and must equal the recording."""
    label = label or "transcript of program %s" % pname
    out = PROGS[pname]["transcript"]
    t = out.split("\n")
    need = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, w, fs, need))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: label %r is too long for a %.2f in panel" % (label, w))
    L = len(t) + (1 if aligned else 0)
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    # aligned: the word 'prints' stands on a line of its own, so that the columns of the transcript line up from its first line on
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": ("\n" + out) if aligned else out,
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


def foot(body, x, y, w, fs=9.5):
    h = round(DS.need_h(body, w, fs) + 0.04, 2)
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states5, "lifecycle": DS.lifecycle_col, "lifecycle_skip": DS.lifecycle_skip, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap





def pair(pname, lines, x, y, wtot, hmax, gap=0.2, lo=7.0, hi=9.0, label=None):
    """A program excerpt (no transcript inside) with its transcript in a panel beside it, at the largest font size at which both fit
    unwrapped in wtot inches and hmax inches; returns (code item, transcript item, bottom y)."""
    pr = PROGS[pname]
    a, b = lines
    t = pr["transcript"].split("\n")
    fs = hi
    while fs >= lo:
        wc = pw(pname, lines, False, fs)
        wc = max(wc, round(len('program %s, lines %d to %d of %d' % (pname, a, b, len(pr['code'].rstrip().split('\n')))) * 0.0725 + 0.12, 2))
        wt = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
        hc = (b - a + 1) * (fs * 1.22 / 72.0 + 0.02) + 0.30
        ht = len(t) * (fs * 1.22 / 72.0 + 0.02) + 0.30
        if wc + gap + wt <= wtot and max(hc, ht) <= hmax:
            c, bot = prog(pname, x, y, wc, fs=fs, lines=lines, show_out=False)
            tr = transcript(pname, round(x + wc + gap, 2), y, wt, fs=fs)
            return c, tr, max(bot, round(y + tr["h"], 2))
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d and their transcript do not fit %.2f x %.2f in side by side at %.1f pt" % (pname, a, b, wtot, hmax, lo))

S = []
SHOWN = {}  # diagram id -> slide number
NOTEXEC = []  # slide numbers that carry the words NOT EXECUTED
MEASURED = []  # slide numbers that show a measured time (and say 'single run')
EMULATED = []  # slide numbers that show an emulation (a Python object standing in for Windows) and say EMULATED


def content(title, sub, items, notes, take, lede=None, notexec=False, measured=False, emulated=False):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 44:
        raise SystemExit("REFUSED: title %r is longer than the 44 characters one line of it holds" % title)
    if len(sub) > 86:
        raise SystemExit("REFUSED: subtitle %r is longer than the 86 characters one line of it holds" % sub)
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
    blob = json.dumps(items)
    if notexec:
        NOTEXEC.append(len(S) + 1)
        if L_NOTEXEC not in blob:
            raise SystemExit("REFUSED: slide %r is declared NOT EXECUTED but says nothing of it" % title)
    if emulated:
        EMULATED.append(len(S) + 1)
        if L_EMU not in blob:
            raise SystemExit("REFUSED: slide %r is declared EMULATED but says nothing of it" % title)
    if measured:
        MEASURED.append(len(S) + 1)
        if L_ONCE not in blob.lower():
            raise SystemExit("REFUSED: slide %r shows a measured time but does not say 'single run'" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


def hidden(pname, a):
    """The words that say where the lines before the excerpt are: lines 1 to a-1 of the program, the corpus HEAD and a comment."""
    return "Lines 1 to %d (imports, a temporary folder, EXAMPLE, save() and a comment) are not shown." % (a - 1)

# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.4, 4.5, fs=10, cap=False)
S.append({"kind": "title", "title": "Ch. 18: CSV, JSON, and XML Files",
          "sub": "Three plain-text formats for data: the csv module, json, xml.etree.ElementTree, and where the chapter and Python differ",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made. What could not be run is marked on its slide.", 0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 17 worked with files that other people made for other people to read. Chapter 18 turns to files that programs read and write: plain text "
                   "in three formats, comma-separated values, JSON and XML, and asks what a program must still do to read them correctly, since all three look like "
                   "text that could simply be split. This deck follows the chapter in its own order: the csv module with its reader and writer, the tab-separated file, the "
                   "DictReader and DictWriter and Project 13 that removes the header row of every CSV file in a folder; JSON with json.loads() and json.dumps(); "
                   "XML with xml.etree.ElementTree and the third-party xmltodict. It adds what the chapter leaves out and what the research found when every printed output was "
                   "run again: Appendix B answers a question about file modes in a way the chapter's own code contradicts, line_num counts lines and not records, "
                   "the chapter never names an encoding, the newline argument has a reason the book calls beyond its scope, JSON refuses or changes several Python values, "
                   "ElementTree does not interpret xsi:nil and reports whitespace, and XML from someone else can be an attack. Everything printed on these slides was produced by "
                   "Python 3.14.6, installed with uv, with xmltodict 1.0.4 and defusedxml 0.7.1; csv, json and ElementTree are the standard library. The programs build their own "
                   "files in a temporary folder and use no network. What could not be run, Microsoft Excel, a real Windows computer and the final release of Python 3.15, "
                   "is marked on its slide, and the one place where a Python object stands in for Windows says EMULATED.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV, "xmltodict 1.0.4", "defusedxml 0.7.1"]}],
        "The first question is the chapter's spine. Each of the three formats imposes rules: a CSV field that holds a comma or a line break must be in quotes, JSON allows six kinds of "
        "value and no trailing comma, and an XML document needs one root element and matching tags. Each has operations that read and write it, the csv reader and writer, json.loads() and "
        "json.dumps(), and ElementTree, and each loses or refuses something: CSV gives back only strings, JSON turns a tuple into a list and refuses a set, and XML read through ElementTree "
        "also gives only strings. All three are plain text that a program must parse and not split. The second question is the watch-out of the deck. The chapter page of 12 October 2026 has "
        "35 listings, 20 of them interactive sessions of 97 statements, and one figure. All 97 statements were replayed in the order of the page under Python 3.14.6. As printed, 89 matched. "
        "The two xml_string listings fail as typed because the closing quotation mark of the xsi namespace is a curly quotation mark, and json_string is wrapped over four lines inside its "
        "quotes, which is a SyntaxError. With the curly quotation mark replaced, 93 matched, and the same came with the versions Appendix A pins, xmltodict 0.13.0 and openpyxl 3.1.5. The "
        "online materials of the book, 91 files, hold exampleWithHeader3.csv and the Excel files but no example3.csv and no XML or JSON file at all, so a reader has to type the files the "
        "chapter opens. Each slide says where a printed line differs and on what evidence. The chips give the size of the chapter as this deck covers it.",
        "Know what each format imposes and loses, and where the book's lines differ.")

# ---- 4 what a program can do with CSV ----------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithCsv", "usecases", (5.0, 1.45, 4.5, 3.15), fs=8)
c, bot = con("csvnames", 0.5, 1.5, 4.3, fs=9, cap=True)
bare = EX["_bare"]["transcript"].split("\n")
content("What a program can do with a CSV file", "Six things through the csv module; the chapter names neither its quoting nor its limit",
        [dg, dcap, c,
         card("Not in the standard library", "In a Python %s with the standard library only: %s; %s. csv imported." %
              (EX["_bare"]["python"], bare[0].replace(" - ", ": "), bare[1].replace(" - ", ": ")),
              0.5, round(bot + 0.15, 2), 4.3, round(4.95 - bot - 0.15, 2), fs=9.5, accent="slate")],
        "The use-case diagram lists what the chapter does with a CSV file through one module: read the rows of a file, write rows to a file, read rows as dictionaries, write dictionaries as "
        "rows, change the delimiter to a tab and, beyond the chapter, read a field above the size limit. They are independent uses of the same module and not a sequence, which is why the picture is "
        "a set of uses. The console beside it lists what the module offers that the chapter never mentions. csv.list_dialects() returns excel, excel-tab and unix; the module has six quoting "
        "constants, QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONE, QUOTE_NONNUMERIC and, since Python 3.12, QUOTE_NOTNULL and QUOTE_STRINGS; and a field may hold at most 131,072 characters. The words QUOTE_, "
        "Sniffer and utf-8-sig are not on the chapter page. The card keeps the line between the standard library and the rest: csv, json and xml.etree.ElementTree come with Python, while xmltodict "
        "and defusedxml, which the XML slides use, do not; in a bare environment of Python 3.14.6 importing either failed with ModuleNotFoundError. The chapter tells the reader to install "
        "xmltodict, and Appendix A pins version 0.13.0 of it while PyPI offered 1.0.4 on the day of the study; the difference matters on the slide about untrusted XML.",
        "csv reads and writes rows and dicts; the chapter shows only a part of it.")

# ---- 5 story: CSV on IBM mainframes -----------------------------------------------------------------------------
c5, bot5 = con("split", 0.5, 2.85, 4.5, fs=8.5, cap=True)
content("CSV before the PC: a 1972 compiler", STORY["CsvFortran1972"]["when"],
        [card("Commas between the values", "The IBM Fortran (level H extended) compiler under OS/360 read free-form input with commas between values in 1972. "
              "An unquoted string could not hold a comma.", 0.5, 1.45, 4.5, 1.3, fs=10.5),
         c5,
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1972: IBM Fortran reads comma-separated input",
             "1978: FORTRAN 77 defines list-directed input",
             "1983: the name CSV is in use",
             "Oct 2005: RFC 4180 writes the format down"]},
         factrow("CsvFortran1972")],
        story_notes("CsvFortran1972") + " The console on the slide uses a shorter line than the study's: the line with a comma inside quotes split into four pieces with split(',') and was "
        "read as three fields by csv.reader. The October 2005 date is the story of RFC 4180, which says each record ends in CRLF, the last record may or may not end in a line break and a header "
        "line is optional; the Python module follows these habits, and the console of the next slides shows the CRLF in the bytes the writer produced.",
        "Never split a CSV line on commas yourself; let csv.reader read it.")

# ---- 6 reading rows ------------------------------------------------------------------------------------------------
dg, dcap = diagram("ReadingACsvFile", "activity", (0.5, 1.4, 4.3, 3.2),
                   grid={"open": (0, 0), "reader": (0, 1), "loop": (0, 2), "row": (0, 3), "more": (0, 4), "again": (0, 5)},
                   cols=[(0.0, 3.3), (3.75, 0.5)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 6},
                   routes={("start", "open"): "h", ("more", "row"): "loopR"}, fs=8, nh=0.34, dh=0.44)
pn = "readerCut_v1_0_0.py"
a6, b6 = span(pn, "save('example.csv', EXAMPLE)")
f6 = bestfs(pn, (a6, b6), 4.55, 3.4)
p6, bot6 = prog(pn, 5.0, 1.55, pw(pn, (a6, b6), True, f6), fs=f6, lines=(a6, b6), show_out=True)
content("Reading rows: a reader and a for loop", "list() or a for loop; every value is a string; line_num counts lines",
        [dg, dcap, p6],
        "This is the chapter's own sequence for reading a file: open the file, pass the file object to csv.reader(), loop over the reader and read each row as a list of strings, and ask "
        "whether another row is left. The program runs it on a file of four records. list(reader) gives four lists, and every value in them is a string, which is why a number read from a "
        "CSV file needs int() or float(). A reader can be looped over once: the second list() on the same reader returned an empty list, so reading the file again means calling open() and "
        "csv.reader() again. A reader has no len() and no index, and the program prints False for both. The loop prints reader.line_num with each row, and the numbers are 1, 2, 3 and 5: "
        "Carol's city holds a line break inside quotes, so her record spans two lines and the reader has read five lines when it hands the record over. line_num is the number of lines "
        "read from the file and not the number of records, which is what the Python documentation says, and Project 13 comes back to it. The file the chapter opens, example3.csv, is not in "
        "the online materials: the zip holds exampleWithHeader3.csv with CRLF line ends and the year 2025 in its timestamps where the chapter prints 2035. This deck's file is the sample "
        "EXAMPLE of the corpus, written by the program, with a quoted comma, a doubled quote and the line break.",
        "A reader gives lists of strings, once; line_num is not the record number.")

# ---- 7 memory ----------------------------------------------------------------------------------------------------------
pn = "memoryCut_v1_0_0.py"
a7, b7 = span(pn, "import tracemalloc")
f7 = bestfs(pn, (a7, b7), 5.6, 3.0)
w7 = pw(pn, (a7, b7), True, f7)
p7, bot7 = prog(pn, 0.5, 1.55, w7, fs=f7, lines=(a7, b7), show_out=True)
x7 = round(0.5 + w7 + 0.25, 2)
content("A for loop against list(): memory", "The chapter says a loop saves memory with a big file; the research measured it",
        [p7,
         {"t": "stat", "x": x7, "y": 1.5, "w": round(9.5 - x7, 2), "h": 1.95, "vert": True, "items": [
             {"n": "69.0 MiB", "label": "peak of list(reader), 300,000 rows"},
             {"n": "0.166 MiB", "label": "peak of a for loop over the same file"}]},
         card("Single run, research", "A generated file of 300,000 rows (7.5 MB), measured once with tracemalloc: a ratio of 416. "
              "This deck's program uses 60,000 rows and prints only whether list() peaks above ten times the loop.", x7, 3.55, round(9.5 - x7, 2), 1.4, fs=9, accent="orange"),
         foot(hidden(pn, a7), 0.5, round(bot7 + 0.08, 2), w7, fs=8.5)],
        "The chapter says that looping over the reader object, instead of calling list() on it, is how to save memory with a big file. The claim holds. The program writes a file of 60,000 rows "
        "and reads it both ways under tracemalloc, which records the peak memory Python allocated: it prints that both readings found 60,000 rows and that the peak of list() is more than "
        "ten times the peak of the loop. The numbers on the slide are the research's, from one run on a generated file of 300,000 rows of 7.5 MB: the peak was 69.0 MiB for list(reader) "
        "and 0.166 MiB for a for loop, a ratio of 416, and the loop was also faster in that run, 0.40 s against 0.90 s; a DictReader loop took 1.22 s. Those are single runs on one machine, "
        "they vary with the machine, and no check of the deck repeats them; the program of the deck prints only the comparison, which it checks every time it is built. A reader object "
        "holds the position in the file and a loop keeps one row at a time, which is also why the reader can be read once. The Python documentation page on tracemalloc describes the tool.",
        "Loop over the reader when the file is big; list() holds every row.", measured=True)

# ---- 8 Appendix B ----------------------------------------------------------------------------------------------------
c8, bot8 = con("appb", 0.5, 1.45, 9.0, fs=10.5, cap=True)
y8 = round(bot8 + 0.12, 2)
content("Appendix B and the chapter disagree", "Question 3 says binary mode; the chapter's code and Python say text mode",
        [c8,
         card("What Appendix B says", "To question 3, the modes of the File objects for Reader and Writer objects, it answers read-binary (rb) and write-binary (wb).",
              0.5, y8, 4.4, round(4.95 - y8, 2), fs=10.5, accent="orange"),
         card("What the chapter and Python do", "The chapter writes open('output.csv', 'w', newline='') and open('example3.csv'), both text mode. "
              "The console shows what rb and wb give.", 5.1, y8, 4.4, round(4.95 - y8, 2), fs=10.5, accent="slate")],
        "The console uses a bytes buffer, which stands for a file opened in binary mode, and a string buffer, which stands for one opened in text mode. csv.reader on bytes raised Error: iterator "
        "should return strings, not bytes, with the advice that the file should be opened in text mode, and csv.writer on a bytes buffer raised TypeError: a bytes-like object is required, not "
        "'str'. The same rows from a string buffer gave the list a and b. So the answer printed in Appendix B for question 3 is contradicted by the chapter's own listings and by Python 3.14.6. "
        "The research found three more places where the book disagrees with itself or with its files. The answer to question 1 is right: in Excel, spreadsheets can have values of data "
        "types other than strings. The chapter says that XML syntax is similar to HTML, which we covered in Chapter 18, but Chapter 18 is this chapter, and HTML is the subject of Chapter 13 "
        "on web scraping. And the Practice Program tells the reader to unzip excelSpreadsheets.zip and test an Excel-to-CSV converter on it, but that zip holds 26 files that are already CSV, "
        "spreadsheet-A.csv to spreadsheet-Z.csv, and no .xlsx file. The lesson for a reader is to run the code and to trust the module's error messages over a one-line answer in an appendix.",
        "Open CSV files in text mode with newline=''; Appendix B's rb and wb are wrong.")

# ---- 9 writing rows ----------------------------------------------------------------------------------------------------
dg, dcap = diagram("WritingACsvFileOnWindows", "sequence", (0.5, 1.45, 4.4, 3.15), fs=8, head_w=1.15)
pn = "writerCut_v1_0_0.py"
a9, b9 = span(pn, "with open('o.csv'")
f9 = bestfs(pn, (a9, b9), 4.4, 3.0)
p9, bot9 = prog(pn, 5.1, 1.55, pw(pn, (a9, b9), True, f9), fs=f9, lines=(a9, b9), show_out=True)
content("Writing rows: the writer and its types", "writerow() returns the length written; None becomes an empty field",
        [dg, dcap, p9, foot(hidden(pn, a9), 5.1, round(bot9 + 0.08, 2), 4.4, fs=8.5)],
        "The sequence diagram is the chapter's way of writing rows: the program calls open() with newline='' and gets the file object, calls csv.writer() with the file object and gets the "
        "writer, and calls writerow() with a list, which writes the row to the file and returns the length. The transcript runs it. writerow() returned 21, 32 and 19, the number of characters "
        "written including the line end. The first row wrote spam,eggs,bacon,ham; the second wrote the quoted field "
        "\"Hello, world!\" because it holds a comma; the third turned the number 3.141592 into its text, None into an empty field and True into the word True. The writer converts everything with "
        "str() and the reader gives back strings, so a number, a None and a bool do not come back as what they were. Every line ends in \\r\\n, the line end that RFC 4180 names, which the "
        "next slide explains. The second part writes a tab-separated file with delimiter='\\t' and lineterminator='\\n' and writerows(), which takes a list of rows; the chapter's tab example "
        "changes the delimiter and the line terminator in the same way.",
        "writerow() returns the length; the reader gives back only strings.")

# ---- 10 newline ------------------------------------------------------------------------------------------------------------
pn = "newlineCut_v1_0_0.py"
a10, b10 = span(pn, "for label, nl in")
f10 = bestfs(pn, (a10, b10), 4.8, 3.0)
w10 = pw(pn, (a10, b10), True, f10)
p10, bot10 = prog(pn, 0.5, 1.55, w10, fs=f10, lines=(a10, b10), show_out=True)
x10 = round(0.5 + w10 + 0.25, 2)
content("newline='' and the double-spaced file", "Why a file written without newline='' shows a blank row between rows on Windows",
        [p10,
         card("EMULATED, not a Windows computer", "csv.writer ends a record with \\r\\n; Windows turns each \\n into \\r\\n, giving \\r\\r\\n. "
              "A TextIOWrapper asked for that translation stands in for it.", x10, 1.5, round(9.5 - x10, 2), 1.55, fs=9.5, accent="orange"),
         card("NOT EXECUTED here", "Microsoft Excel and a real Windows machine were not run. LibreOffice 24.2 opened a file of that kind with the layout of Figure 18-1: "
              "rows 1, 3 and 5 filled, 2 and 4 empty.", x10, 3.15, round(9.5 - x10, 2), 1.6, fs=9.5, accent="orange"),
         foot(hidden(pn, a10) + " The two comment lines above the loop are not shown either.", 0.5, round(bot10 + 0.08, 2), w10, fs=8.5)],
        "The chapter says that on Windows a file for a reader or writer must be opened with newline='' or the rows of output.csv will be double-spaced, shows Figure 18-1, and says the reason is "
        "beyond the book. The reason is short. csv.writer ends every record with the two characters CR and LF. A file opened in text mode without the newline argument translates every line feed "
        "it is given to the line end of the platform, and on Windows that is CR LF, so the CR LF of the writer becomes CR CR LF. The program reproduces the translation by asking io.TextIOWrapper "
        "for it, which is why the slide says EMULATED: it is not a Windows computer. With newline='' the bytes were a,b CR LF and csv.reader returned one row; with the translation they were "
        "a,b CR CR LF and csv.reader returned the row followed by an empty row. The research opened such a file in LibreOffice 24.2, the program that stood in for Excel, and saw the "
        "layout of Figure 18-1; Microsoft Excel and a real Windows machine were NOT EXECUTED, and nothing on this slide is claimed about how Excel shows the file. The Python "
        "documentation says a file given to csv.reader or csv.writer should be opened with newline='' and that it should always be safe to specify it, because the csv module does its own "
        "universal newline handling. The alt text of the figure in the chapter, a screenshot of a Windows desktop with six overlapping calculators, does not describe it: the picture is a spreadsheet.",
        "Always pass newline='' to open() for csv; the module handles line ends itself.", notexec=True, emulated=True)

# ---- 11 DictReader and DictWriter ---------------------------------------------------------------------------------------------
pn = "dictsCut_v1_0_0.py"
a11, b11 = span(pn, "save('example.csv'")
f11 = bestfs(pn, (a11, b11), 6.0, 3.4)
w11 = pw(pn, (a11, b11), True, f11)
p11, bot11 = prog(pn, 0.5, 1.55, w11, fs=f11, lines=(a11, b11), show_out=True)
x11 = round(0.5 + w11 + 0.25, 2)
content("DictReader and DictWriter", "The first row gives the keys; short rows get None, long rows go under the key None",
        [p11,
         card("What a row can do", "A short row has None for the missing key, a long row keeps its extras under the key None. "
              "restkey and restval rename them.", x11, 1.5, round(9.5 - x11, 2), 1.45, fs=9.5, accent="slate"),
         card("The writer refuses keys", "A key that is not in fieldnames raises ValueError. "
              "writeheader() and writerow() return the length.", x11, 3.05, round(9.5 - x11, 2), 1.3, fs=9.5, accent="orange"),
         ],
        "DictReader uses the first row of the file as the keys of every following row, so a program reads row['Name'] and not row[0]. The program writes a file whose rows do not all have the "
        "same length. The second row, Bob, has no age, and DictReader gave None for the key Age; the third row has two values more than the header, and DictReader put them in a list under "
        "the key None. Naming them with restkey='rest' and filling the missing value with restval='?' gave a tidy dictionary for every row. The chapter mentions neither argument. DictWriter "
        "takes the file and the list of field names; writeheader() returned 10, the length of Name,Age and its line end, and writerow() returned 8 for Dave and 6 for Eve, whose missing Age "
        "was written as an empty field. A row with a key that is not in fieldnames, City, raised ValueError: dict contains fields not in fieldnames: 'City', which the chapter also never shows. In the shipped exampleWithHeader3.csv the first list "
        "printed in the chapter has six dictionaries where the file has seven data rows.",
        "Name the extras with restkey and restval; the writer refuses unknown keys.")

# ---- 12 quoting, dialects, limits ---------------------------------------------------------------------------------------------------
tq = EX["_tables"]["quotingConstants"]["rows"]
tbl = {"t": "table", "x": 0.5, "y": 1.5, "w": 4.6, "colW": [1.55, 3.05], "fs": 9.5, "rowH": 0.33, "rows": tq}
c12, bot12 = con("limits", 5.25, 1.5, 4.25, fs=8, cap=True)
content("Quoting, dialects and the field limit", "Six quoting constants write one row six ways; the limit is 131,072 characters",
        [tbl, c12,
         card("The row written", "One row per constant; QUOTE_NONE needs an escapechar.", 0.5, 3.95, 4.6, 1.0, fs=9.5, accent="slate")],
        "The chapter does not mention the quoting constants, and the table shows what they do. The same row, a b, c,d, the number 7, None and an empty string, was written six times. "
        "QUOTE_MINIMAL, the default, quotes only the field with the comma and writes None and the empty string alike as an empty field. QUOTE_ALL quotes every field, so 7 becomes \"7\". "
        "QUOTE_NONNUMERIC quotes every field that is not a number. QUOTE_NONE never quotes, so the comma needs an escape character and the writer put a backslash before it. "
        "QUOTE_STRINGS and QUOTE_NOTNULL were added in Python 3.12 and do not exist in 3.11, the research found by running eleven interpreters: QUOTE_STRINGS quotes strings and "
        "writes None as an empty field and the empty string as \"\", which is the difference that lets a reader tell them apart. The console shows the read side: with QUOTE_NOTNULL "
        "an unquoted empty field is read as None and a quoted one as an empty string. A field larger than csv.field_size_limit(), 131,072 characters, raises csv.Error: a field of "
        "131,073 characters did. The dialect excel-tab reads a tab-separated row as the two fields a and b. The module also has a Sniffer, skipinitialspace, strict "
        "and escapechar, which the chapter does not name either.",
        "Pick the quoting constant for the data; QUOTE_NOTNULL tells None from ''.")

# ---- 13 encoding -----------------------------------------------------------------------------------------------------------------------
pn = "encodingCut_v1_0_0.py"
a13, b13 = span(pn, "text = ")
f13 = bestfs(pn, (a13, b13), 5.3, 3.0)
w13 = pw(pn, (a13, b13), True, f13)
p13, bot13 = prog(pn, 0.5, 1.55, w13, fs=f13, lines=(a13, b13), show_out=True)
x13 = round(0.5 + w13 + 0.25, 2)
content("The encoding the chapter never names", "Excel's UTF-8 CSV starts with a BOM; open() needs encoding= to read it right",
        [p13,
         card("Default encoding", "Without encoding=, open() uses the locale: UTF-8 on this machine, cp1252 for most Windows "
              "users in the United States.", x13, 1.5, round(9.5 - x13, 2), 1.5, fs=9.5, accent="slate"),
         card("NOT EXECUTED here", "Python 3.15.0 final and Python 3.14.7 or later were not run. Only 3.15.0b4 was: UTF-8 mode on by default (PEP 686), "
              "where 3.14.6 gave 0.", x13, 3.1, round(9.5 - x13, 2), 1.7, fs=9.5, accent="orange"),
         foot(hidden(pn, a13), 0.5, round(bot13 + 0.08, 2), w13, fs=8.5)],
        "Every listing of the chapter calls open() without an encoding, and the chapter does not mention encodings. In text mode the encoding is then the locale encoding, which is UTF-8 here "
        "and is cp1252 for most Windows users in the United States. The program writes a file the way Excel saves CSV UTF-8, with the three bytes EF BB BF in front, the byte order mark, and "
        "reads it back three ways. Opened with encoding='utf-8' the first line begins with the invisible character \\ufeff, and DictReader makes it part of the first key, which the program prints as \\ufeffName and not "
        "Name; encoding='utf-8-sig' removes it. The same bytes decoded as cp1252 give the mojibake that starts with the characters ï»¿. A file saved in cp1254, the Turkish "
        "Windows encoding, and read as UTF-8 raises UnicodeDecodeError: invalid continuation byte. The answer is to name the encoding of the file when you open it. Python 3.15 changes the "
        "default: the research ran 3.15.0b4, installed with uv, and sys.flags.utf8_mode was 1 where Python 3.11 to 3.14.6 gave 0, because PEP 686 makes UTF-8 mode the default. "
        "python.org lists 3.15.0 as released on 9 October 2026 and 3.14.7 and 3.14.8 as released, but uv offered only 3.15.0b4 and 3.14.6 on the day, so the final release and the "
        "later 3.14 releases were NOT EXECUTED, and nothing on this slide is claimed about them.",
        "Name the encoding when you open a CSV file; utf-8-sig removes Excel's BOM.", notexec=True)

# ---- 14 Project 13 ------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("RemovingCsvHeaders", "activity", (0.5, 1.4, 4.2, 3.2),
                   grid={"find": (0, 0), "reader": (0, 1), "skip": (0, 2), "write": (0, 3), "more": (0, 4)},
                   cols=[(0.0, 3.3), (3.7, 0.5)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 5},
                   routes={("start", "find"): "h", ("more", "reader"): "loopR"}, fs=8, nh=0.34, dh=0.44)
pn = "project13Cut_v1_0_0.py"
a14, b14 = span(pn, "from pathlib")
f14 = bestfs(pn, (a14, b14), 4.7, 3.4)
p14, bot14 = prog(pn, 4.85, 1.55, pw(pn, (a14, b14), True, f14), fs=f14, lines=(a14, b14), show_out=True)
content("Project 13: remove the header row", "next(reader, None) skips the header record; line_num != 1 skips a line",
        [dg, dcap, p14],
        "Project 13 is the chapter's second program built from steps: loop through the files whose names end in .csv, read each with csv.reader() and skip the first row, and write the other "
        "rows to a new file in a folder called headerRemoved. The activity diagram has one choice, whether another file is left, and the program follows it. The program here runs the steps on "
        "generated files and adds a file the chapter does not test, an empty one. next(reader, None) skips the header record whatever its length and does not fail on the "
        "empty file: the file with a header and two rows gave the two rows, and the empty file gave an empty output file; the corpus program also tests a file with only a header, which gave an empty output file too. The chapter skips the header with a test of reader.line_num, keeping "
        "a row only when line_num is not 1. The last lines of the program show the trap: a header cell that holds a line break, written with quotes, ends at line_num 2, so the test kept "
        "both records and the header was still there. On the 100 shipped files in removeCsvHeader.zip, which have one-line headers and no embedded line breaks, the program as written is "
        "right: every output equals the input without its first record, 19,631 records in and 19,531 out. The practice program at the end of the chapter, the Excel-to-CSV converter, was "
        "written to its skeleton and run in the research with openpyxl 3.1.5, not by this deck. The skeleton is not a program, since its loop has no indented body and it uses names it "
        "never defines. The converter wrote the dates of the workbooks as 2035-04-05 13:34:02, not 4/5/2035 13:34, because openpyxl returns datetime objects and csv.writer writes their "
        "text. The skeleton also evaluates sheet.max_column inside the row loop, and each evaluation visits every cell of the sheet: on produceSales3.xlsx, with 23,758 rows and 4 columns, the first 2,000 rows took 5.94 s that way and 0.006 s with the limit hoisted; those are single runs of the research, they vary with the machine, and the slowdown grows with rows times cells. The converter wrote 5 CSV files from 3 workbooks.",
        "Skip the header with next(reader, None), not with line_num.")

# ---- 15 story: the first JSON message ------------------------------------------------------------------------------
c15, bot15 = con("jsonstrict", 0.5, 2.85, 9.0, fs=10, cap=True)
content("JSON: a message sent in April 2001", STORY["JsonMessage2001"]["when"],
        [card("A message from a start-up", "Douglas Crockford sent the first JSON message with Chip Morningstar at State Software, "
              "a company cofounded in March 2001.", 0.5, 1.45, 4.7, 1.3, fs=10.5),
         c15,
         {"t": "beats", "x": 5.4, "y": 1.5, "w": 4.1, "h": 1.2, "fs": 11, "items": [
             "Apr 2001: the first JSON message",
             "2006: RFC 4627 describes it",
             "2013: ECMA-404 standardizes it",
             "2017: RFC 8259, the current standard"]},
         factrow("JsonMessage2001")],
        story_notes("JsonMessage2001") + " The console shows the strictness in the chapter's own example: json.loads() of a list of two words gave the list, and the same list with a comma before the "
        "closing bracket raised JSONDecodeError: Illegal trailing comma before end of array: line 1 column 16. The message depends on the release: Python 3.11 and 3.12 said Expecting value, and the "
        "trailing-comma message is from 3.13, as the research found by running eleven interpreters. Single quotes failed too, with Expecting property name enclosed in double quotes. "
        "The Python documentation still names RFC 7159 as the specification, which RFC 8259 obsoleted in December 2017.",
        "JSON is tiny and strict; one extra comma is an error.")

# ---- 16 JSON syntax ------------------------------------------------------------------------------------------------------
pn = "jsonBasicsCut_v1_0_0.py"
a16, b16 = span(pn, "js = ")
f16 = bestfs(pn, (a16, b16), 4.4, 3.0)
w16 = pw(pn, (a16, b16), True, f16)
p16, bot16 = prog(pn, 0.5, 1.55, w16, fs=f16, lines=(a16, b16), show_out=True)
x16 = round(0.5 + w16 + 0.25, 2)
tj = EX["_tables"]["jsonRefusals"]["rows"]
tbl = {"t": "table", "x": x16, "y": 1.5, "w": round(9.5 - x16, 2), "colW": [1.65, round(9.5 - x16 - 1.65, 2)], "fs": 9, "rowH": 0.34, "rows": tj}
content("JSON syntax: strict by design", "Six value types; json.loads refuses a trailing comma, single quotes and comments",
        [p16, tbl,
         foot(hidden(pn, a16), 0.5, round(bot16 + 0.08, 2), w16, fs=8.5),
         card("Python accepts NaN", "[NaN] was accepted; RFC 8259 does not allow NaN, Infinity or -Infinity.",
              x16, 3.95, round(9.5 - x16, 2), 1.0, fs=9, accent="orange")],
        "JSON has six kinds of value: an object, an array, a string, a number, true or false, and null. The program parses the chapter's kind of text: null became None, true became True, and "
        "the result is a dict. json.dumps() of that dict equals the original text when the keys are in the same order and the default separators are used, and indent=2 puts one item on each "
        "line. The table is computed, not typed: for each text it calls json.loads() and prints what the module says. The chapter tells the reader that trailing commas, single quotes and "
        "comments are not allowed, and all of it holds under Python 3.14.6: the list with a trailing comma fails at column 16, the single-quoted key at column 2, and the comment after the object "
        "as Extra data at column 10. None, the Python word, is not JSON and fails at column 2; an empty text fails at column 1. One thing the chapter does not say is in the last line of the "
        "table: Python accepts NaN, and also Infinity and -Infinity, which RFC 8259 does not allow, so a file with them is valid for Python and invalid for other parsers. The messages differ "
        "by release: Expecting value in 3.11 and 3.12 where 3.13 and later say what is wrong with the comma. The format is small enough to describe on one page, json.org does it.",
        "Python's json accepts NaN; the standard does not.")

# ---- 17 a value through JSON --------------------------------------------------------------------------------------------------
dg, dcap = diagram("AValueThroughJson", "lifecycle_skip", (0.5, 1.4, 4.6, 3.2), fs=8, sw=1.4, sh=0.38, sfs=9, top=0.28, lab_w=1.5, margin=1.35)
pn = "jsonTypesCut_v1_0_0.py"
a17, b17 = span(pn, "d = {")
f17 = bestfs(pn, (a17, b17), 4.3, 3.0)
p17, bot17 = prog(pn, 5.2, 1.55, pw(pn, (a17, b17), True, f17), fs=f17, lines=(a17, b17), show_out=True)
content("A Python value through JSON", "A tuple comes back as a list, int and None keys as strings; a set or bytes raises",
        [dg, dcap, p17, foot(hidden(pn, a17), 5.2, round(bot17 + 0.08, 2), 4.3, fs=8.5)],
        "The state diagram follows one Python value. json.dumps() turns the value into JSON text; for a type it does not support, such as a set, it raises an error and the value stays what it was. "
        "The text can be written to a file, and json.loads() turns the text, or the text read back from the file, into a Python value again, with the changes the format makes. The transcript runs "
        "them. A dict with the tuple (1, 2), the integer key 1 and the key None was written as {\"t\": [1, 2], \"1\": \"a\", \"null\": \"c\"} and read back as {'t': [1, 2], '1': 'a', 'null': 'c'}: the "
        "tuple became a list and did not come back, and the keys 1 and None became the strings 1 and null. The chapter does not say any of this. By default json.dumps() writes non-ASCII "
        "characters as escapes, so the capital I with a dot became \\u0130, and ensure_ascii=False keeps the character. A set, bytes and a complex number raise TypeError: Object of type set is not "
        "JSON serializable, and so on, and a dict key that is a tuple raises TypeError: keys must be str, int, float, bool or None, not tuple. The same list of changes explains why a round trip "
        "through JSON is not a copy: what comes back is built only from the six JSON kinds.",
        "A round trip through JSON returns only the six kinds of JSON value.")

# ---- 18 JSON gaps -----------------------------------------------------------------------------------------------------------------------
pn = "jsonGapsCut_v1_0_0.py"
a18, b18 = span(pn, "print(json.dumps(float('nan'))")
c18, t18, bot = pair(pn, (a18, b18), 0.5, 1.55, 9.0, 2.75)
content("JSON gaps: NaN, BOM and 4,300 digits", "Files, a BOM in bytes and in text, an integer limit, and the notes of Python 3.14",
        [c18, t18,
         foot(hidden(pn, a18), 0.5, round(bot + 0.06, 2), 9.0, fs=8.5),
         foot("The chapter has no json.load() or json.dump(): it reads and writes strings only, and the file forms are not on its page. Python 3.14 names the path to a value that cannot be written.",
              0.5, round(bot + 0.4, 2), 9.0, fs=10)],
        "The program shows five things the chapter leaves out. First, Python writes NaN for float('nan') and reads Infinity as inf, which is not JSON. Second, json.dump() and json.load() "
        "write and read a file directly; neither name is on the chapter page, which uses only the string functions. The file holds the bytes of UTF-8, with the capital I with a dot as the two "
        "bytes c4 b0 because ensure_ascii=False was passed, and reading it back gave the same dict with None and True. Third, json.loads() accepts bytes that begin with the UTF-8 byte order mark "
        "and decodes them, while a str that begins with the mark raises JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig). Fourth, a string of 5,000 digits exceeds the limit of "
        "4,300 digits for converting a string to int, and json.loads() raised ValueError, because Python limits the conversion to protect against slow attacks. Fifth, Python 3.14 adds notes "
        "to the TypeError of a serialization error that name the path to the value that failed: for a set inside a list inside a dict the notes were when serializing dict item 'a' and when "
        "serializing list item 1. Under Python 3.11 to 3.13 the notes are absent, and python -m json, which pretty-prints JSON from the command line, is allowed from 3.14. Python 3.15 adds "
        "an array_hook parameter to load() and loads(); the research ran only 3.15.0b4, so that is not shown here.",
        "Use json.load() and dump() for files; a BOM breaks str, not bytes.")

# ---- 19 what a program can do with XML ------------------------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithElementTree", "usecases", (0.5, 1.45, 3.9, 3.15), fs=8)
pn = "etReadCut_v1_0_0.py"
a19, b19 = span(pn, "import xml.etree")
f19 = bestfs(pn, (a19, b19), 5.0, 3.4)
p19, bot19 = prog(pn, 4.5, 1.55, pw(pn, (a19, b19), True, f19), fs=f19, lines=(a19, b19), show_out=True)
content("What a program can do with XML", "Seven things through ElementTree; the text of an element is a string or None",
        [dg, dcap, p19],
        "The use-case diagram lists what the chapter does with XML through xml.etree.ElementTree: read the root and its children, read the text of an element, iterate over the elements in document "
        "order, find elements with find() and findall(), add a SubElement and set an attribute, indent the tree to print it, and, beyond the chapter, clear elements while iterparse reads a "
        "large file. The program reads a compact document. fromstring() returns the root, whose tag is person; iterating over it gives its six children; root[0].text is the string Alice Doe; "
        "the text of the self-closing car element is None, as the chapter says. iter() returns the root first and then every descendant in document order, so the list has eight tags. find() "
        "takes a path such as address/city and a small subset of XPath such as phone[@type=\"work\"], returns None when nothing matches, and findall() returns a list; ElementTree has no xpath() "
        "method, which lxml has. Every text is a str: age is the string 30 and needs int(). The chapter's listings print None for address and phone, which holds for the compact string and not "
        "for the pretty-printed file, as the next slide shows. ElementTree entered the standard library with Python 2.5 on 19 September 2006, from Fredrik Lundh's library, and json with Python 2.6 "
        "on 1 October 2008, from Bob Ippolito's simplejson; the old calls getchildren() and getiterator() of older tutorials are gone in Python 3.14.6.",
        "ElementTree gives strings and None; find() returns None when nothing matches.")

# ---- 20 whitespace, truth, errors, iterparse -----------------------------------------------------------------------------------------------
pn = "etTrapsCut_v1_0_0.py"
a20, b20 = span(pn, "import warnings")
c20, t20, bot = pair(pn, (a20, b20), 0.5, 1.55, 9.0, 3.0)
content("ElementTree: whitespace, truth, errors", "Pretty-printed XML has text between tags; bool(element) warns; iterparse frees memory",
        [c20, t20,
         foot(hidden(pn, a20), 0.5, round(bot + 0.06, 2), 9.0, fs=8.5),
         foot("Well-formed is not valid: the chapter calls a document with several roots not valid, the W3C word is not well-formed, and ElementTree never checks validity against a DTD.",
              0.5, round(bot + 0.4, 2), 9.0, fs=10)],
        "The program runs four statements of the chapter that Python answers differently. The chapter says whitespace outside the tags is insignificant, but ElementTree reports it: in a "
        "pretty-printed document the text of an element that holds only elements is the whitespace between the tags, and the tail of an element is the whitespace after it, which is why the "
        "chapter's loop printed None for address and phone for a compact string and a line of whitespace for the pretty-printed file. Second, an element is false when it has no children, "
        "and since Python 3.12 testing it emits a DeprecationWarning, so a result of find() must be tested with is None. The transcript shows False and the warning. Third, the errors: "
        "<a><b></a> is a mismatched tag, two roots are junk after the document element, <A></a> is a mismatched tag because tag names are case sensitive, and an attribute value with no quotes "
        "is not well-formed. The chapter says tag and attribute names can be written in any case, which holds only when the end tag matches the start tag. The chapter also calls a document with "
        "several roots not valid; the W3C word for a document that obeys the syntax is well-formed, and valid means compliance with a document type declaration, which ElementTree never checks. "
        "Fourth, iterparse reads a file as it goes and clearing each element after use keeps the memory small; here it printed an end event for each i and then for the root r, whose text "
        "is None. The research found that the parser returned by iterparse gained a close() method in Python 3.13.",
        "Test find() with is None; ElementTree keeps whitespace and checks no schema.")

# ---- 21 writing XML, namespaces and xsi:nil -------------------------------------------------------------------------------------------------------
pn1, pn2 = "etWriteCut_v1_0_0.py", "etNamespaceCut_v1_0_0.py"
a21, b21 = span(pn1, "import xml.etree")
a21b, b21b = span(pn2, "import xml.etree")
f21a = bestfs(pn1, (a21, b21), 4.3, 3.0, hi=7.5)
w21a = pw(pn1, (a21, b21), True, f21a)
p21a, bot21a = prog(pn1, 0.5, 1.55, w21a, fs=f21a, lines=(a21, b21), show_out=True)
x21 = round(0.5 + w21a + 0.2, 2)
f21b = bestfs(pn2, (a21b, b21b), round(9.5 - x21, 2), 3.0, hi=7.5)
p21b, bot21b = prog(pn2, x21, 1.55, round(9.5 - x21, 2), fs=f21b, lines=(a21b, b21b), show_out=True)
content("Writing XML, namespaces and xsi:nil", "tostring() writes a space before the slash; ElementTree never reads xsi:nil",
        [p21a, p21b,
         foot(hidden(pn1, a21) + " Both programs are cut the same way. The element boat is marked xsi:nil and still holds the text full.",
              0.5, round(max(bot21a, bot21b) + 0.08, 2), 9.0, fs=9)],
        "On the left the program builds a tree with Element, SubElement and set(), as the chapter does. ET.tostring() writes an empty element with a space before the slash, <car xsi:nil=\"true\" />, "
        "where the chapter prints it without; with the default encoding it returns bytes, and encoding='unicode' returns a str; the characters < and & in the text of the note were escaped as &lt; and "
        "&amp;. ET.indent(), added in Python 3.9, pretty-prints the tree in place. The last line shows the trap of the chapter's own example: tostring() writes an attribute named xsi:nil with no check "
        "that the prefix xsi is declared, and parsing the result again fails with ParseError: unbound prefix. On the right the program reads a document that declares the prefix. ElementTree stores a namespaced "
        "attribute under its full name, {http://www.w3.org/2001/XMLSchema-instance}nil, drops xmlns:xsi from the attributes, and never turns nil into None: the element car, marked nil and empty, has "
        "text None because it is empty, and the element boat, marked nil, kept its text full, although the XML Schema specification says such an element must be empty for the document to be valid. A "
        "namespaced name is part of the tag, {http://example.org/a}i, and find('i') finds only the element with no namespace; find() with a prefix needs the namespaces dictionary. xmltodict, on "
        "the slide after, keeps @xsi:nil as a key of a dict, so car is a dict and not None.",
        "A namespace is part of the name; declare the prefix before you write it.")

# ---- 22 xmltodict ---------------------------------------------------------------------------------------------------------------------------------
pn = "xmltodictCut_v1_0_0.py"
a22, b22 = span(pn, "import xmltodict")
f22 = bestfs(pn, (a22, b22), 5.0, 3.4)
w22 = pw(pn, (a22, b22), True, f22)
p22, bot22 = prog(pn, 0.5, 1.55, w22, fs=f22, lines=(a22, b22), show_out=True)
x22 = round(0.5 + w22 + 0.25, 2)
ch = EX["_charts"]["formatSizes"]
chart = {"t": "chart", "ctype": "bar", "x": x22, "y": 1.45, "w": round(9.5 - x22, 2), "h": 2.45, "labels": ch["labels"],
         "title": "characters for the same person", "series": [{"name": "characters", "data": ch["values"]}], "dataLabels": True, "dlFs": 9}
content("xmltodict: XML as a dict of strings", "One entry is a value, several a list; attributes get @; and the size of two formats",
        [p22, chart,
         foot("The chart is computed: the chapter's person as JSON and as XML (the XML with its xmlns:xsi declaration, 407 characters compact). " + hidden(pn, a22),
              x22, 3.95, round(9.5 - x22, 2), fs=8)],
        "xmltodict is a third-party package that turns XML into a dict, and the chapter uses it. The program parses a person: every value is a string, age is '30'; the element phone has an "
        "attribute, so it becomes a dict with the key @type and the text under #text. One b under a gives the value '1', two b elements give a list, which is the trap of the package: a program "
        "that reads d['a']['b'] gets a string or a list depending on the data. force_list=('b',) makes it a list every time. unparse() turns the dict back into XML, with pretty=True it indents "
        "with tabs, and the round trip parse(unparse(d)) equals d; an empty element <b/> becomes None. The chart is computed from the research's person: compact JSON is 248 characters, "
        "indent=2 makes it 326, the XML without whitespace is 407, 1.64 times the JSON, and after ET.indent() it is 496. JSON keeps int, bool and null across a round trip; XML through "
        "ElementTree or xmltodict and CSV give strings only. The version matters: xmltodict 1.0.4, installed here, was released on 22 February 2026, and Appendix A pins 0.13.0 of 8 May 2022.",
        "xmltodict gives strings, a value or a list, and @ for attributes.")

# ---- 23 XML from someone else -------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ParsingUntrustedXml", "activity", (0.5, 1.4, 4.3, 3.2),
                   grid={"text": (0, 0), "trust": (0, 1), "parse": (0, 2), "defused": (1, 2), "forbid": (1, 3), "error": (1, 4), "use": (0, 4)},
                   cols=[(0.0, 2.0), (2.25, 2.05)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 5},
                   routes={("start", "text"): "h", ("trust", "defused"): "hv", ("forbid", "use"): "hv"}, fs=8, nh=0.34, dh=0.5)
pn = "securityCut_v1_0_0.py"
a23, b23 = span(pn, "import xml.etree")
f23 = bestfs(pn, (a23, b23), 4.6, 3.0)
p23, bot23 = prog(pn, 4.95, 1.55, pw(pn, (a23, b23), True, f23), fs=f23, lines=(a23, b23), show_out=True)
pins = EX["_pins"]["transcript"].split("\n")
content("XML from someone else", "ElementTree refuses a billion laughs; defusedxml refuses entities; xmltodict varies",
        [dg, dcap, p23,
         foot("xmltodict by version: 1.0.4 raises ValueError: entities are disabled; 0.13.0, the version Appendix A pins, parsed both documents (a pins-environment run).",
              4.95, round(bot23 + 0.1, 2), 4.55, fs=9)],
        "The chapter parses XML with ET.fromstring() and xmltodict.parse() and never says that XML from a source you do not trust can be an attack. The flow chart has the choices: if the text came from "
        "a source you trust, parse it with ET.fromstring(); if not, parse it with defusedxml, ask whether the document has an entity, and catch the exception that forbids it. The program "
        "runs the cases. A small document with entities that expand ten times each, three levels deep, is expanded by ElementTree into a text of 300 characters; defusedxml raised EntitiesForbidden "
        "for the same document. A billion laughs document of ten levels, 539 bytes here and 760 bytes in the research, would expand to three billion characters; ElementTree under Python 3.14.6, "
        "which bundles Expat 2.8.1, refused it with limit on input amplification factor breached; the Python documentation says Expat versions lower than 2.7.2 may be vulnerable, and "
        "Python 3.14.0 to 3.14.5 carry 2.6.3 and 3.11 to 3.13 carry 2.6.1. An external entity that names a file was not read; ElementTree reported an undefined entity. The attack is catalogued as CWE-776 "
        "and external entities as CWE-611. xmltodict 1.0.4 refuses every entity with ValueError: entities are disabled, while xmltodict 0.13.0, the version Appendix A pins, parsed both documents "
        "of the program in the pins environment and returned a dict without the entity text. Wikipedia dates the billion laughs attack to as early as 2002, widely addressed from 2008: "
        "the story is in the notes, not on a slide.",
        "Parse untrusted XML with defusedxml, and keep the parser up to date.")

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("CsvJsonAndXmlAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The CSV format comes first: a field in quotes can hold a comma, a doubled quote is an escape, and the encoding is not named. The csv module follows: a "
        "reader gives rows of strings and can be looped over once, and a writer needs newline=''. JSON: a trailing comma is refused, a tuple becomes a list and keys become strings. XML: tags are "
        "case sensitive, a namespace is part of a name, and xsi:nil is not understood. The XML libraries branch: the text of an element is None or a string, xmltodict gives strings, and iterparse "
        "clears elements. The last branch is the book and its practice: Project 13 removes headers, next() skips the header, and the chapter has a curly quote. Together they answer the first "
        "question of the chapter, what each format imposes and loses, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 18 - free online", PUB["P01"][2]],
         ["csv module documentation", PUB["P07"][2]],
         ["json module documentation", PUB["P08"][2]]]
_ref = [["xml.etree.ElementTree documentation", PUB["P09"][2]],
        ["XML security in Python (documentation)", PUB["P10"][2]],
        ["RFC 4180: the CSV format", PUB["P28"][2]],
        ["RFC 8259: the JSON standard", PUB["P29"][2]]]
_hist = [["CSV and IBM Fortran (Wikipedia)", STORY["CsvFortran1972"]["link"]],
         ["JSON and Douglas Crockford (Wikipedia)", STORY["JsonMessage2001"]["link"]],
         ["XML 1.0 and the W3C (Wikipedia)", STORY["Xml10In1998"]["link"]],
         ["ElementTree enters Python 2.5 (What's New)", STORY["PythonLibraries2006"]["link"]],
         ["The billion laughs attack (Wikipedia)", STORY["BillionLaughs2002"]["link"]]]
_pkg = [["defusedxml on PyPI", PUB["P43"][2]],
        ["xmltodict on PyPI", PUB["P40"][2]]]
LINKS = [r[1] for r in _read + _ref + _hist + _pkg]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist},
            {"head": "The two packages", "rows": _pkg}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the "
        "chapter; the documentation of the three modules describes them. The reference links are the pages for the topics where the deck corrected or extended the chapter: the XML security page of the "
        "Python documentation, the RFCs that write down CSV and JSON, and the two third-party packages. The history links are the sources behind the six stories of the chapter. Two of them are slides, "
        "the IBM Fortran compiler of 1972 and the first JSON message of April 2001; the other four are told in the notes: RFC 4180 of October 2005 on the slide of the quoting constants, XML 1.0 of "
        "10 February 1998 on the slide that reads XML, ElementTree and json entering the standard library in 2006 and 2008 on the same slide, and the billion laughs attack on the slide of XML from "
        "someone else. The rest of the sixty-odd sources of the research, among them the W3C recommendations, the PEPs and the CWE entries, are in the research package.",
        "Textbook, module documentation and history, opened the day this deck was built.")

# ---- 26 closing ---------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "Open CSV files in text mode with newline='' and an encoding, and loop over the reader.",
            "A reader gives strings and line_num counts lines, so use next() to skip a header.",
            "JSON refuses a trailing comma, turns a tuple into a list and keeps only six kinds of value.",
            "ElementTree gives strings and keeps whitespace; parse untrusted XML with defusedxml."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The console rows use only text and io objects made "
        "in memory, so they can be typed into any Python; csv, json and ElementTree are the standard library, and the programs build their own files in a temporary folder. The rows were run again under "
        "Python 3.14.6 with xmltodict 1.0.4 and defusedxml 0.7.1 each time the deck was built, and the programs were run again by the check that compares the slides with the recording. What was not run is "
        "marked on its slide: Microsoft Excel and a real Windows computer, and the final release of Python 3.15 with Python 3.14.7 and later. The next chapter of the book keeps time, schedules tasks and "
        "launches programs, and what this chapter taught about formats, encodings and the difference between a file made to be parsed and text that only looks parseable carries over.",
        "Questions are welcome; bring a CSV, a JSON or an XML file to open.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The CSV format and reading it", "What a program can do with a CSV file", "Appendix B and the chapter disagree"),
          ("Writing CSV, and the details around it", "Writing rows: the writer and its types", "Project 13: remove the header row"),
          ("JSON", "JSON: a message sent in April 2001", "JSON gaps: NaN, BOM and 4,300 digits"),
          ("XML with ElementTree", "What a program can do with XML", "Writing XML, namespaces and xsi:nil"),
          ("xmltodict, and XML you did not write", "xmltodict: XML as a dict of strings", "XML from someone else"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, 6 - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, 6 - _nstory)},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from a comma in quotes to a billion laughs."
S[1]["notes"] = ("The route has six parts. It starts with CSV: what a program can do with the csv module, the 1972 compiler that read commas between values, the reader and its single pass, "
                 "the memory a for loop saves, and the place where Appendix B disagrees with the chapter. Then writing CSV and the details around it: the writer and its types, the newline argument "
                 "and the double-spaced file, DictReader and DictWriter, the quoting constants and the field limit, the encoding the chapter never names, and Project 13 with the header row. "
                 "Then JSON: the first message of April 2001, the syntax Python refuses, a value through dumps and loads, and the gaps of NaN, the byte order mark and the 4,300-digit limit. Then XML "
                 "with ElementTree: what a program can do with it, whitespace, the truth value and iterparse, and writing XML with namespaces and xsi:nil. The fifth part is xmltodict and XML that "
                 "someone else wrote, with the billion laughs. The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Two of "
                 "the slides are true stories and four more are told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. Every "
                 "output was printed by Python 3.14.6 with xmltodict 1.0.4 and defusedxml 0.7.1, and what could not be run is marked on its slide.")

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
plan = {"meta": {"title": "Ch. 18: CSV, JSON, and XML Files", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "measured": MEASURED, "emulated": EMULATED}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; measured", MEASURED, "; emulated", EMULATED)
