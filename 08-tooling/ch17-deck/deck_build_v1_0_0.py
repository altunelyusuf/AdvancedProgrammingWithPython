#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 17 (PDF and Word Documents) on the CME classroom standard.

Same regime as chapters 10 to 16: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources,
full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their
line numbers) with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with pypdf 6.20.1, python-docx 1.2.0, pdfminer.six
20260107, Pillow 12.3.0 and cryptography 50.0.2); the speaker notes are prose for the reader and carry only what the chapter's RDODI
research package (03-materials/ch17/rdodi, sen0414_ch17_rdodi_data_v1_0_1.py, findings F1 to F15), its records
(08-tooling/ch17-page/*.json) or a program of this deck established.

What this chapter adds against chapter 16: the programs need two packages beyond the standard library (and three optional ones), so the
deck is run with the research interpreter, not a bare one; the files the programs work on are made by the programs themselves (a small
valid PDF written byte by byte, Word documents written by python-docx) except two files the book ships (Recursion_Chapter1.pdf and
demo.docx), which two programs fetch from nostarch.com on their first run and check against their sha256 (they are LIVE, and every
slide that shows one says so, as honesty_check_v1_0_0.py requires). The worst-case timings of the Password Breaker are the research
record's single runs and are marked as such on their slide. What could not be run - the language-model clean-up of the section
Post-Processing with AI, Microsoft Word and a PDF viewer - is marked NOT EXECUTED on its slide. The eight narrative diagrams of the chapter
(sen0414_ch17_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py, with a column-of-states
diagram added for the life of an encrypted PDF) and checked by diagram_check_v1_0_0.py; one table (the algorithms of encrypt()) and one chart
(the rotation of a page after four calls) are native PowerPoint objects whose data the deck check computes again; no photograph is used,
because the research could not fetch and licence one (Wikimedia Commons answered 429); two of the six stories are slides (the Camelot
memo and the ZIP format) and four are told in the notes.

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


ST = load("stories17", os.path.join(HERE, "..", "sen0414_ch17_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams17", os.path.join(HERE, "..", "sen0414_ch17_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi17", os.path.join(HERE, "..", "sen0414_ch17_rdodi_data_v1_0_1.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s, %s" % (PYV, EX["_packages"].split(" | ")[0] + ", " + EX["_packages"].split(" | ")[1])
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires the LIVE words of a program on every slide that shows it, and 'single run' on
# every slide that shows a measured time)
L_LIVE_PDF = ("Shipped file: Recursion_Chapter1.pdf of the book's online materials, fetched from nostarch.com at run time, "
              "sha256 d943896e0bd2... checked.")
L_LIVE_DOCX = ("Shipped file: demo.docx of the book's online materials, fetched from nostarch.com at run time, "
               "sha256 b43b21137d7d... checked.")
L_NOTEXEC = "NOT EXECUTED"
L_ONCE = "single run"


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
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states5, "lifecycle": DS.lifecycle_col, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
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


def content(title, sub, items, notes, take, lede=None, notexec=False, measured=False):
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
    if measured:
        MEASURED.append(len(S) + 1)
        if L_ONCE not in blob.lower():
            raise SystemExit("REFUSED: slide %r shows a measured time but does not say 'single run'" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


def live(pnames):
    """True when any of the programs is LIVE (the slide then needs L_LIVE)."""
    return any(EX["_programs"][p]["kind"] == "live" for p in pnames)




def hidden(pname, a):
    """The words that say where the lines before the excerpt are: lines 1 to a-1 of the program, the corpus helper make_pdf() and imports."""
    return "Lines 1 to %d of the program (the helper make_pdf(), which writes a small valid PDF 1.4 of text pages byte by byte, and the imports) are not shown." % (a - 1)


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.4, 4.5, fs=10, cap=False)
S.append({"kind": "title", "title": "Ch. 17: PDF and Word Documents",
          "sub": "Documents made for people to read: pypdf for PDF files, python-docx for Word files, and what neither can do",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made. The two files the book ships were fetched and hash-checked; what could not be run is marked on its slide.", 0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 16 kept data in one database file that a program owns. Chapter 17 turns to the opposite case: files that other people made for "
                   "other people to read, a PDF that looks the same on every screen and a Word document that opens in an editor, and asks what a program "
                   "can do with them. This deck follows the chapter in its own order: the PDF package pypdf, which reads text and images, copies pages "
                   "into a new file, rotates and inserts pages, lays one page over another and encrypts a file; Project 12 that combines the pages of "
                   "many PDFs; the Word package python-docx, which reads paragraphs and runs, styles them, and writes paragraphs, headings, breaks and "
                   "pictures; and the three practice programs, PDF Paranoia, Custom Invitations and PDF Password Breaker. It adds what the chapter leaves "
                   "out and what the research found when every printed output was run again: the default encryption of pypdf is RC4 and not AES-256, "
                   "the merge() line of the chapter inserts the whole file, rotations add up, insert_blank_page(2) means a width of two points, "
                   "most of the attributes of Table 17-1 belong to the font and not to the run, the text of a hyperlink is in no run, a style name with a "
                   "trailing space raises KeyError, the package docx cannot be imported, and the dictionary of the Password Breaker is eight times the size "
                   "the page names. Everything printed on these slides was produced by Python 3.14.6, installed with uv, with pypdf 6.20.1 and python-docx 1.2.0; "
                   "the programs build their own documents, and the only network use is the fetch of the two files the book ships, whose hashes are checked.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV, "pypdf 6.20.1", "python-docx 1.2.0"]}],
        "The first question is the chapter's spine, and it is a question about limits. A PDF stores drawing commands that put words on a page, and a .docx "
        "file is a ZIP archive of XML parts, so a program can read the paragraphs and runs of a Word file, write a new one, copy, reorder, rotate, stamp "
        "and encrypt the pages of a PDF, and extract its text and images, but it cannot recover structure that was never stored: there are no paragraphs in a "
        "PDF, text comes out in the order it was drawn, a scanned page has no text at all and a black box drawn over words does not remove them. The second "
        "question is the watch-out of the deck. The chapter's 91 interactive statements were replayed one by one on the files the book ships under "
        "Python 3.14.6 with pypdf 6.20.1 and python-docx 1.2.0: 89 printed what the page prints and 2 differed, both in the third run of the demo paragraph. "
        "Under the versions Appendix A pins, pypdf 5.0.1 and python-docx 1.1.2, 88 matched and 3 differed. The agreement is smaller than it looks, because a "
        "statement that prints nothing cannot differ from the page, and the merge() example of the chapter is such a statement: it prints nothing and does "
        "not do what the chapter says. Each slide says where a printed line differs and on what evidence. The chips give the size of the chapter as this "
        "deck covers it: six branches, the topics beneath them, the console rows and the programs that were run, the eight diagrams, and the Python and "
        "package releases that printed every result.",
        "Know what a program can do with these files, and where the book's lines differ.")

# ---- 4 what a program can do with a PDF ----------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithPdfs", "usecases", (5.0, 1.45, 4.5, 3.15), fs=8)
c, bot = con("names", 0.5, 1.5, 4.3, fs=9, cap=True)
content("What a program can do with a PDF", "Eight things through pypdf; the names older tutorials use are gone",
        [dg, dcap, c,
         card("One library, three names", "pyPdf (2005), PyPDF2 (2011) and pypdf are one library; a tutorial that names PdfFileReader or PdfMerger fails.",
              0.5, round(bot + 0.15, 2), 4.3, round(4.95 - bot - 0.15, 2), fs=9.5, accent="slate")],
        "The use-case diagram lists what the chapter does with a PDF through one package: extract the text of the pages, extract the images of a page, copy pages into a "
        "new file, insert pages at a position, rotate pages, merge a watermark under a page, and encrypt and decrypt a file with a password. They are independent "
        "uses of the same module and not a sequence, which is why the picture is a set of uses. The console beside it shows the first trap of the chapter, which is "
        "about names. The package the chapter uses is pypdf, written in lower case, and its two classes are PdfReader and PdfWriter; PdfFileReader and PdfFileWriter, "
        "which many older tutorials use, and PdfMerger are not attributes of pypdf 6.20.1, so a program copied from such a tutorial raises AttributeError. The story "
        "is in the documentation of pypdf. Mathieu Fenniak launched pyPdf in 2005, whose last release was 1.13 in 2010; at the end of 2011 Phaseit sponsored PyPDF2 as a "
        "fork; Martin Thoma took over its maintenance in April 2022; and PyPDF2 was merged back into pypdf, all lower case and without a number. PdfMerger was removed in "
        "pypdf 5.0.0. The study found the same on ten interpreters, Python 3.11, 3.12, 3.13 and the seven releases 3.14.0 to 3.14.6, so the behaviour of these packages "
        "does not depend on the 3.x release. Two optional packages, Pillow for images and cryptography for AES, are not named by the chapter and appear on later slides.",
        "Use pypdf and PdfReader; the names older tutorials teach no longer exist.")

# ---- 5 story: Warnock -----------------------------------------------------------------------------------------------------
content("A 1991 memo called Camelot", STORY["WarnockCamelot1991"]["when"],
        [card("A page that looks the same", "John Warnock, co-founder of Adobe, outlined a system called Camelot in the spring of 1991. Its goal was to "
              "capture documents from any application, send them anywhere, and view and print them on any machine.", 0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Spring 1991: Warnock outlines Camelot",
             "15 Jun 1993: the first Acrobat is released",
             "A file ends with an offset and %%EOF",
             "Its text is drawing commands, not paragraphs"]},
         factrow("WarnockCamelot1991")],
        story_notes("WarnockCamelot1991") + " Two of the facts on the slide were read in the study itself: a small PDF written for it began with %PDF-1.4 and ended "
        "with %%EOF, and the words of its page were the drawing command BT /F1 18 Tf 72 720 Td (Page one) Tj ET. The next slide runs both.",
        "A PDF is a page description made to look the same on every machine.")

# ---- 6 structure of a PDF ----------------------------------------------------------------------------------------------------
pn = "structureCut_v1_0_0.py"
a6, b6 = span(pn, "data = make_pdf('Page one'")
c6, t6, bot = pair(pn, (a6, b6), 0.5, 1.55, 9.0, 3.0)
content("Header, table and drawing commands", "What a PDF file holds, and why text comes out in stream order",
        [c6, t6, foot(hidden(pn, a6) + " The black box is a filled rectangle drawn after the line of text.", 0.5, round(bot + 0.08, 2), 9.0, fs=9)],
        "The program writes a two-page PDF by hand and takes it apart with the standard library. The file starts with the header %PDF-1.4 and ends with %%EOF. The word "
        "startxref near the end gives a byte offset, and at that offset the bytes xref begin the cross-reference table, which lists the offset of every numbered object: "
        "the table of this file has 8 entries, object 0 is the free one, and the first three offsets point at the text 1 0 obj, 2 0 obj and 3 0 obj. A reader finds the "
        "table by reading the last lines, so pypdf can open a file by jumping to the end first. The words of a page are not stored as paragraphs. They are drawing commands in "
        "a content stream, BT /F1 18 Tf 72 720 Td (Page one) Tj ET, and get_contents().get_data() returns those same bytes. Two consequences follow, and both were run. "
        "Text comes out in the order of the commands and not in the order of the page: with (world) drawn first at x 200 and (Hello) drawn second at x 72, extract_text() "
        "returned worldHello, while extraction_mode='layout' returned Hello and world apart. And a black rectangle drawn over a line hides it from the eye and not from a "
        "program: extract_text() still returned Salary: 120000 USD, and the Wikipedia article on redaction says the same of PDF files. PDF 1.7 became an international "
        "standard as ISO 32000-1 in July 2008, as the Library of Congress describes it; the file the book calls Recursion_Chapter1.pdf is PDF version 1.6 made by Adobe InDesign.",
        "A PDF holds drawing commands, read in the order they were drawn.")

# ---- 7 reading text -------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ReadingAPdfToText", "activity", (0.5, 1.4, 4.3, 3.2),
                   grid={"open": (0, 0), "failed": (0, 1), "loop": (0, 2), "extract": (0, 3), "join": (0, 4), "write": (0, 5), "fallback": (1, 1)},
                   cols=[(0.0, 2.3), (2.64, 1.66)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 6},
                   routes={("start", "open"): "h", ("fallback", "write"): "vh"}, fs=8, nh=0.34, dh=0.44)
pn = "extractTextCut_v1_0_0.py"
a7, b7 = span(pn, "from pdfminer.high_level")
f7 = bestfs(pn, (a7, b7), 4.5, 3.4)
p7, bot7 = prog(pn, 5.0, 1.55, pw(pn, (a7, b7), True, f7), fs=f7, lines=(a7, b7), show_out=True)
content("Reading text, page by page", "pypdf adds the pages with nothing between them; pdfminer.six and layout mode differ",
        [dg, dcap, p7],
        "This is the chapter's own sequence for extracting text: open the file in binary read mode, build a PdfReader, loop over reader.pages, call extract_text() on each "
        "page and add the strings, and write the text to a file; the chapter's listing falls back on pdfminer.six when pypdf cannot understand the file. The program runs "
        "the middle of it on a six-page file. Adding the strings with += gives Page 1Page 2Page 3Page 4Page 5Page 6, with nothing between the pages, which is also what "
        "happens on the shipped chapter: the last words of page 1, Al Sweigart, run into the 2 of page 2 as Al Sweigart2; joining with a newline keeps them apart. "
        "pdfminer.six returns the same text with a form feed after every page, 6 in all, and on the shipped chapter it returned 33,200 characters against pypdf's 32,981 and "
        "spaced out the chapter heading as W H A T. Layout mode keeps the horizontal gap between the columns of a table-like page, so Name and Price stay in their columns, "
        "where the default joins the words of a row with single spaces. The fallback was not needed: of eleven damaged files given to both libraries, none was read by "
        "pdfminer.six and refused by pypdf, four were refused by both. The text script the book ships, run on the sample chapter, wrote 32,981 characters in 688 lines, and "
        "printed 11 warnings that name the optional package fontTools.",
        "Join pages yourself, and choose the extraction mode that matches the page.")

# ---- 8 post-processing with AI: NOT EXECUTED -------------------------------------------------------------------------------------------------------------
c, bot = con("hyphen", 0.5, 1.5, 4.6, fs=10, cap=True)
content("Post-processing with AI", "A hyphen repair by a regular expression was run; the language-model clean-up was not",
        [c,
         card("NOT EXECUTED here", "The chapter's section Post-Processing with AI sends extracted text to a language model to clean it. No model was called "
              "for this deck, so nothing is claimed about what one returns.", 5.4, 1.45, 4.1, 1.75, fs=10, accent="orange"),
         card("A repair that is deterministic", "re.sub of a hyphen followed by a newline joins follow- and ing the execution, and it also glues "
              "well-known into wellknown. pypdf's documentation calls post-processing outside its scope.", 5.4, 3.3, 4.1, 1.65, fs=10, accent="slate"),
         {"t": "text", "x": 0.5, "y": round(bot + 0.05, 2), "w": 4.6, "h": round(4.97 - bot - 0.05, 2), "fs": 11, "color": "ink",
          "body": "Extracted text keeps the hyphens and row breaks of the printed page; repairing it is a separate step."}],
        "Extracted text keeps the hyphens and the row breaks of the printed page. A page with follow- at the end of one row and ing the execution on the next came out of "
        "pypdf with a newline between them, and re.sub of a hyphen and a newline gave following the execution. That repair is deterministic, and the console runs it, but "
        "it is not harmless: the same expression turns well-known, written over two rows, into wellknown, because a regular expression cannot tell a hyphen the typesetter "
        "added from one that belongs to the word. The chapter's own answer is a section called Post-Processing with AI, which sends the text to a language model and asks it "
        "to clean the text. That section was NOT EXECUTED in this study and is not run for this deck: no model was called, and the slide therefore claims nothing about "
        "what a model returns. The documentation of pypdf, in its page on post-processing of text extraction, says the matter is outside the scope of the library and "
        "lists dehyphenation among the steps a program takes after extraction. A scanned page raises the same question in a harder form, and the next slide runs it: it has "
        "no text to clean at all.",
        "Repairing extracted text is your step; the language-model way was not run.", notexec=True)

# ---- 9 images, scans and the book's PDF ---------------------------------------------------------------------------------------------------------------
pn = "shippedChapterPdfCut_v1_0_0.py"
a9, b9 = span(pn, "name = real_file(")
f9 = bestfs(pn, (a9, b9), 4.55, 3.0)
w9 = pw(pn, (a9, b9), True, f9)
p9, bot9 = prog(pn, 0.5, 1.55, w9, fs=f9, lines=(a9, b9), show_out=True)
x9 = round(0.5 + w9 + 0.25, 2)
c9, bot = con("scan", x9, 1.55, round(9.5 - x9, 2), fs=9, cap=True)
content("Images, scans and the book's PDF", "The chapter's image loop on the sample chapter; a scanned page has images and no text",
        [p9, c9,
         foot(L_LIVE_PDF + " Page images need the Pillow package, which the chapter does not name.", 0.5, round(max(bot9, bot) + 0.12, 2), 9.0, fs=9)],
        "The program is the chapter's loop on the file the book ships. Recursion_Chapter1.pdf has 18 pages, is not encrypted, and its first page begins 1, WHAT IS RECURSION?; "
        "the images per page, printed as separate numbers, are 7 2 1 0 0 0 1 and then zeros, and the loop writes 11 files. The file is the one the program fetches from the online materials of the "
        "third edition and checks against its sha256 before it opens a copy. The study found two differences from the page. The sample output the chapter prints says that "
        "page 7 is skipped with not enough image data, and neither the newest releases nor the versions Appendix A pins skipped it: both wrote 10_page7_Im0.tif. And the loop "
        "needs the Pillow package, which the chapter never names: without it reading an image raises ImportError, pillow is required to do image extraction, as the bare "
        "environment of the study printed. The console builds a page that is only a picture: a 40 by 40 pixel image saved as PDF has one page, extract_text() returns the "
        "empty string and the page holds one image named image.jpg whose data begins with the JPEG marker FF D8, which is what a scanned document looks like to the library. "
        "There is no text to repair and nothing to extract without optical character recognition, which pypdf does not do. An empty file raises EmptyFileError and a file cut "
        "off before its xref table raises PdfStreamError. The zip of the online materials holds the PDF and the Word file the chapter reads but not encrypted.pdf, "
        "helloworld.docx or restyled.docx, which the chapter names as files the reader makes.",
        "Images need Pillow, and a scan gives you images and an empty string.")

# ---- 10 copying pages --------------------------------------------------------------------------------------------------------------------------------------
pn = "pageSelectionCut_v1_0_0.py"
a10, b10 = span(pn, "six = make_pdf(")
f10 = bestfs(pn, (a10, b10), 5.9, 3.4)
w10 = pw(pn, (a10, b10), True, f10)
p10, bot10 = prog(pn, 0.5, 1.55, w10, fs=f10, lines=(a10, b10), show_out=True)
x10 = round(0.5 + w10 + 0.25, 2)
content("Copying pages: a tuple is a range", "append() reads a tuple as a range and a list as pages; merge() reads it as a title",
        [p10,
         card("A tuple is a range", "(0, 5) copies five pages, (0, 5, 2) every second one, [0, 5] exactly two. "
              "A page past the end raises IndexError.", x10, 1.5, round(9.5 - x10, 2), 1.3, fs=9.5, accent="slate"),
         card("The merge() trap", "The chapter's line inserts the whole file: the tuple became a bookmark title. "
              "Write pages=(0, 2).", x10, 2.9, round(9.5 - x10, 2), 1.4, fs=9.5, accent="orange"),
         foot(hidden(pn, a10), x10, 4.38, round(9.5 - x10, 2), fs=8.5)],
        "The program copies pages of a six-page file into a new writer. A tuple of two numbers selects pages the way range() does, so append(file, (0, 5)) copies Page 1 "
        "to Page 5 and not the sixth, which is why the chapter's first-five-pages example works; a tuple of three adds a step, so (0, 5, 2) copies Page 1, Page 3 and "
        "Page 5; and a list names pages exactly, so [0, 5] copies Page 1 and Page 6. A page number past the end raises IndexError, Sequence index out of range, for the tuple "
        "and the list alike. merge() takes the position first and puts the copied pages there: merging the pages (0, 2) of the six-page file at position 1 of a "
        "three-page writer gave A1, Page 1, Page 2, A2, A3. Written as the chapter writes it, merge(1, file, (0, 2)), the tuple lands in the parameter outline_item, "
        "which the signature types as a title only, so pypdf made a bookmark titled (0, 2) and inserted the whole six-page file: the writer ended with 9 pages and not 5. "
        "On the shipped chapter the same line took a writer of 5 pages to 23, identically on the ten interpreters, because the file has 18; append() accepts the tuple in its "
        "second place because there the parameter may be a title or a page range. The line prints nothing, so the replay of the chapter's statements counted it as a match. "
        "Under the pinned pypdf 5.0.1 the same line raises AttributeError, tuple object has no attribute startswith. The pypdf documentation has a page on merging.",
        "Write pages=(0, 2) for merge(); a bare tuple becomes a bookmark title.")

# ---- 11 rotate, blank pages, watermark -----------------------------------------------------------------------------------------------------------------------
pn = "rotateBlankWatermarkCut_v1_0_0.py"
a11, b11 = span(pn, "w = pypdf.PdfWriter(); w.append(")
f11 = bestfs(pn, (a11, b11), 6.0, 3.4)
w11 = pw(pn, (a11, b11), True, f11)
p11, bot11 = prog(pn, 0.5, 1.55, w11, fs=f11, lines=(a11, b11), show_out=True)
ch = EX["_charts"]["rotationSum"]
x11 = round(0.5 + w11 + 0.25, 2)
chart = {"t": "chart", "ctype": "bar", "x": x11, "y": 1.45, "w": round(9.5 - x11, 2), "h": 2.45, "labels": ch["labels"],
         "title": "page.rotation after each call", "series": [{"name": "degrees", "data": ch["values"]}], "dataLabels": True, "dlFs": 9}
content("Rotate, blank pages and a watermark", "Rotations add up, a blank page copies a neighbour's size, over=False lays under",
        [p11, chart,
         foot("The chart is computed: the stored rotation after rotate(90), rotate(270), rotate(-90) and rotate(180). " + hidden(pn, a11), x11, 3.95,
              round(9.5 - x11, 2), fs=8.5)],
        "rotate() takes a multiple of 90, changes the page in place and returns it; rotate(45) raises ValueError, Rotation angle must be a multiple of 90. The angles add "
        "up and the sum is never reduced to a turn: after rotate(90), rotate(270), rotate(-90) and rotate(180) the stored rotations were 90, 360, 270 and 450, and a negative "
        "angle is stored as it was given. The chart draws these four numbers, computed again when the deck is checked. A new blank page takes its size from a page already "
        "in the writer: after pages of 300 by 400 and 100 by 100 points, insert_blank_page(index=1) made a page of 100 by 100, and add_blank_page() after a 200 by 200 "
        "page made another 200 by 200. The signature of insert_blank_page is width, height, index, so a single positional number is the width: insert_blank_page(2) made a "
        "page 2 points wide, while index=2 made a page of the normal 612 points. The chapter writes insert_blank_page(2). A watermark "
        "is a page laid over or under another with merge_page(): with over=False the watermark's drawing commands come before the page's own, MARK then BASE, so the "
        "mark lies under the text, and the default over=True puts them after, BASE then MARK. merge_page() changes the page it is called on and returns None.",
        "Rotation keeps adding up, and insert_blank_page(2) sets a width.")

# ---- 12 encrypt: RC4 default ------------------------------------------------------------------------------------------------------------------------------------
tb = EX["_tables"]["encryptAlgorithms"]["rows"]
tbl = {"t": "table", "x": 0.5, "y": 1.5, "w": 5.0, "colW": [2.3, 0.8, 0.8, 1.1], "fs": 10.5, "rowH": 0.34, "rows": tb}
bare = EX["_bare"]["transcript"].split("\n")
content("Encrypt: RC4 is the default", "encrypt() without an algorithm writes RC4; the chapter shows only AES-256",
        [tbl,
         card("The chapter shows one form", "encrypt('swordfish', algorithm='AES-256') wrote V 5, R 6 and a 256-bit key. "
              "Without the algorithm the file is RC4 with a 128-bit key.", 0.5, 3.1, 5.0, 1.8, fs=11, accent="slate"),
         card("AES needs a package", "In an environment with pypdf alone (Python %s): %s; %s." % (EX["_bare"]["python"], bare[1].replace(" - ", ": "), bare[2]),
              5.8, 1.5, 3.7, 1.75, fs=10, accent="orange"),
         card("Words the chapter never uses", "Pillow, cryptography and DependencyError are absent from the page; Appendix A pins pypdf 5.0.1 and python-docx 1.1.2.",
              5.8, 3.35, 3.7, 1.55, fs=10, accent="slate")],
        "The table is computed, not typed: for each call the program writes a one-page file, reads the document's /Encrypt dictionary back with pypdf and prints its encryption "
        "version V, its revision R and its key length. encrypt('swordfish') with no algorithm wrote RC4 with a 128-bit key, V 2 and R 3, and no crypt filter dictionary; "
        "algorithm='AES-128' wrote V 4, R 4; algorithm='AES-256' wrote V 5, R 6 and a key length of 256, which is what the chapter recommends and the only form it shows. The "
        "research also asked the command line tool qpdf, which reported AESv3 for the AES-256 file. Two optional dependencies matter in practice. AES needs the cryptography package: "
        "in the environment with pypdf alone, algorithm='AES-256' failed at encrypt() with DependencyError, cryptography>=3.1 is required for AES algorithm, while the "
        "default RC4 was written; AES-128 fails later, at write(). The images of the previous slide need Pillow. The chapter's text names neither package, and the versions "
        "the book pins are given only in Appendix A, pypdf 5.0.1 and python-docx 1.1.2, while PyPI offered pypdf 6.20.1 and python-docx 1.2.0 on the day of the study. An attempt "
        "to install the pinned Pillow 10.4.0 for Python 3.14 found no wheel and the build failed for lack of the libjpeg headers, so that environment used the newest Pillow. "
        "The pypdf documentation has a page on encryption and decryption.",
        "Ask for AES-256 by name, and install cryptography to get it.")

# ---- 13 decrypt: the life of an encrypted PDF ----------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AnEncryptedPdfThroughItsLife", "lifecycle", (0.5, 1.4, 4.6, 3.2), fs=8, sw=1.7, sh=0.42, sfs=9, top=0.3, lab_w=2.4)
pn = "decryptCut_v1_0_0.py"
a13, b13 = span(pn, "w = pypdf.PdfWriter(); w.add_blank_page")
f13 = bestfs(pn, (a13, b13), 4.2, 3.4)
p13, bot13 = prog(pn, 5.3, 1.55, pw(pn, (a13, b13), True, f13), fs=f13, lines=(a13, b13), show_out=True)
content("Decrypt: the life of an encrypted PDF", "A reader refuses its pages until decrypt() matches a password",
        [dg, dcap, p13],
        "The state diagram follows one PDF. A plain PDF becomes an encrypted file when a writer encrypts it with a password and writes the file. A reader that opens the file "
        "is not decrypted: is_encrypted is True, and asking for pages[0] raises FileNotDecryptedError, File has not been decrypted. decrypt() returns a value that says which "
        "password matched: USER_PASSWORD for the user password, OWNER_PASSWORD for the owner password and NOT_DECRYPTED for a wrong password, an empty one or one with different capitals, "
        "and it raises nothing for a wrong password, so a program must read the returned name; the transcript runs these cases. Once decrypt() matches, the reader gives its pages, "
        "and a writer that appends them and writes a new file makes a decrypted copy. encrypt('pw') with one password sets it for both roles, so decrypt('pw') returned OWNER_PASSWORD. "
        "A file encrypted with an empty user password and another owner password opens without a decrypt() call, and the owner password still returns OWNER_PASSWORD. The "
        "program uses a blank page because the point is the password and not the text; it builds its file in memory. The study also ran pdftotext without the password, which refused the "
        "encrypted file, and with it, which read it; that is the research's observation of a second program and is not repeated here.",
        "decrypt() returns which password matched; read it, because it never raises.")

# ---- 14 Project 12 ----------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("CombiningManyPdfs", "activity", (0.5, 1.4, 4.3, 3.2),
                   grid={"find": (0, 0), "sort": (0, 1), "writer": (0, 2), "open": (0, 3), "copy": (0, 4), "more": (0, 5), "save": (0, 6)},
                   cols=[(0.0, 3.3), (3.75, 0.5)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 6},
                   routes={("start", "find"): "h", ("more", "open"): "loopR"}, fs=8, nh=0.34, dh=0.44)
pn = "combinePdfsCut_v1_0_0.py"
a14, b14 = span(pn, "for name in ('b.pdf'")
f14 = bestfs(pn, (a14, b14), 4.55, 3.4)
p14, bot14 = prog(pn, 5.0, 1.55, pw(pn, (a14, b14), True, f14), fs=f14, lines=(a14, b14), show_out=True)
content("Project 12: combine many PDFs", "Every page after the first of each file, in the order of the names, case ignored",
        [dg, dcap, p14],
        "Project 12 is the chapter's first program built from steps: find all the PDF files of the working directory, sort their names without regard to case, open each one, "
        "copy every page after the first into one writer and save the result. The activity diagram has one choice, whether another file is left, and the program follows it. Three "
        "corrections come from the study. As printed, the loop appends to pdf_files, a name never defined, and Python 3.14.6 answers NameError: name 'pdf_files' is not defined, suggesting "
        "pdf_filenames; the shipped combine_pdfs.py is not the finished program either, because it writes PdfWriter without the pypdf prefix and stops at NameError. The test "
        "filename.endswith('.pdf') misses a file named with capitals, which is why the program here lower-cases the name, and the file c.PDF is found. And the program does not guard against "
        "reading its own output: a second run found combined.pdf in the folder and read it as one of its inputs, so the 3 pages of the first run became 5 here (the research's own run went from 5 pages to 9). "
        "Sorting with key=str.lower puts A.pdf before b.pdf, as the diagram says. With the name corrected the program combined three small files into combined.pdf "
        "with every page but the first of each.",
        "Guard Project 12 against its own output, and test file names in lower case.")

# ---- 15 PDF Paranoia ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "pdfParanoiaCut_v1_0_0.py"
a15, b15 = span(pn, "def encrypt_tree(folder, password):", "os.remove(path); print(")
a15b, b15b = span(pn, "def decrypt_tree(folder, password):")
f15a = bestfs(pn, (a15, b15), 4.45, 3.0, out=False, hi=8.0)
w15a = pw(pn, (a15, b15), False, f15a)
p15a, bot15a = prog(pn, 0.5, 1.55, w15a, fs=f15a, lines=(a15, b15), show_out=False)
x15 = round(0.5 + w15a + 0.2, 2)
f15b = bestfs(pn, (a15b, b15b), round(9.5 - x15, 2), 3.35, hi=8.0)
p15b, bot15b = prog(pn, x15, 1.55, round(9.5 - x15, 2), fs=f15b, lines=(a15b, b15b), show_out=True)
content("PDF Paranoia", "Encrypt a tree of PDFs, test each copy, delete the original; then decrypt them",
        [p15a, p15b,
         card("Not on the command line", "Any process list shows a command line (CWE-214), so the chapter's password is visible there.",
              0.5, round(bot15a + 0.08, 2), w15a, 1.03, fs=9.5, accent="orange"),
         foot("Lines 1 to %d: make_pdf(), imports, tree, pdfs()." % (a15 - 1),
              0.5, round(bot15a + 1.14, 2), w15a, fs=8)],
        "The first practice program walks a folder tree with os.walk(), encrypts every PDF with AES-256, saves it with the suffix _encrypted.pdf, opens the new file, decrypts it and "
        "compares the page counts, and only then deletes the original. The second walks the tree again, finds the encrypted files and writes a decrypted copy for the password given, "
        "and for a wrong password prints a message and continues. The transcript is the whole run: three files encrypted and their originals removed, a wrong password that "
        "skips all three and does not stop the program, and three decrypted copies. The folder holds a.pdf, sub/b.pdf, sub/deeper/C.PDF and notes.txt, and the program finds C.PDF "
        "because it tests the lower-cased name: a filter on the lower-case extension .pdf alone misses it. The deck's copy prints shorter lines than the corpus program, and adds one "
        "small generator, pdfs(), for the walk. The chapter asks for the password on the command line. The study notes that any program that lists processes can read a command "
        "line, which is the weakness MITRE names CWE-214, Invocation of Process Using Visible Sensitive Information, so the research's advice is to keep the password of PDF Paranoia out "
        "of the command line. The program deletes an original only after the test; that is why the test comes first.",
        "Test the encrypted copy before deleting; keep passwords off the command line.")

# ---- 16 PDF Password Breaker ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "passwordBreakerCut_v1_0_0.py"
a16, b16 = span(pn, "import time")
f16 = bestfs(pn, (a16, b16), 5.0, 3.4)
w16 = pw(pn, (a16, b16), True, f16)
p16, bot16 = prog(pn, 0.5, 1.55, w16, fs=f16, lines=(a16, b16), show_out=True)
x16 = round(0.5 + w16 + 0.25, 2)
content("PDF Password Breaker, and its worst case", "Both cases of every word until decrypt() succeeds; the file is 8 times the page",
        [p16,
         {"t": "stat", "x": x16, "y": 1.5, "w": round(9.5 - x16, 2), "h": 1.95, "vert": True, "items": [
             {"n": "349,900", "label": "words in the book's dictionary.txt"},
             {"n": "699,800", "label": "attempts, both cases of each word"}]},
         card("Worst case, no match", "RC4 (the default): 241.7 s. AES-256: 1,467.5 s. Two single runs started together on a two-core machine, 12 Oct 2026; "
              "the page names over 44,000 words and 88,000 attempts.", x16, 3.55, round(9.5 - x16, 2), 1.4, fs=9, accent="orange")],
        "The third practice program decrypts a PDF by trying every word of a dictionary, in lower case and in upper case, until decrypt() stops returning NOT_DECRYPTED. The program "
        "here uses a four-word dictionary so that it can run in a blink: the password is CHERRY, found on the sixth attempt, after apple, APPLE, banana, BANANA, cherry; a dictionary of "
        "n words costs up to 2n attempts, 8 for four words. The chapter's file is another size. The dictionary.txt of the online materials has 349,900 lines, all lower-case letters, "
        "between 4 and 12 letters long, which is 8.0 times the 44,000 words the page names, so trying both forms of every line is 699,800 attempts and not the 88,000 of the page. "
        "The worst case, a password that is not in the list, was run to the end on a file written by pypdf 6.20.1: it found nothing and took 241.7 seconds for RC4, the default of "
        "encrypt(), and 1,467.5 seconds for AES-256, the two runs started together on a machine with two cores. A stronger algorithm costs about six times as much per guess, so the "
        "chapter's remark that a long random password defeats the program is shown by the timing and not only stated. The password swordfish, which the chapter uses for its examples, "
        "is not in the dictionary. Both numbers are single runs on one machine on 12 October 2026, they vary with the machine, and they are not repeated by any check of the deck.",
        "A long, random password beats a dictionary; AES-256 makes each guess dearer.", measured=True)

# ---- 17 a .docx is a ZIP of XML (story) ------------------------------------------------------------------------------------------------------------------------------------------------
c17, bot17 = con("zip", 0.5, 1.5, 5.0, fs=8.5, cap=True)
content("A .docx file is a ZIP of XML", STORY["ZipFormat1989"]["when"],
        [c17,
         card("PK, for Phil Katz", "Phil Katz of PKWARE and Gary Conway designed the ZIP format; its first release is dated 14 February 1989. "
              "Office Open XML is extended from it.", 5.7, 1.4, 3.8, 1.5, fs=10, accent="slate"),
         card("python-docx, imported as docx", "The package docx (0.2.4, 6 Feb 2014) fails on import in Python %s: %s." %
              (EX["_docx02"]["python"], EX["_docx02"]["last_line"]), 5.7, 3.0, 3.8, 1.35, fs=10, accent="orange"),
         factrow("ZipFormat1989", y=4.42)],
        story_notes("ZipFormat1989") + " The console shows it: a new python-docx document saved to memory begins with the bytes PK, holds 17 parts, and one of them is "
        "word/document.xml, whose body for one paragraph is <w:p><w:r><w:t>Hello, world!</w:t></w:r></w:p>, a paragraph (w:p) that holds runs (w:r), each holding text (w:t). "
        "That is why a .docx file can be opened with the zipfile module, and why paragraphs and runs are the two words of the Word half of the chapter. The format is a published "
        "standard: Wikipedia gives 7 December 2006 as the first release of Office Open XML, as Ecma standard ECMA-376, and November 2008 for the four-part International Standard "
        "ISO/IEC 29500, after a fast-track process that ended in April 2008. In the study the template that docx.Document() starts from still named python-docx as its author and the year "
        "2013, had no paragraphs, one section and 164 styles. The chapter says to install Python-Docx, not Docx, and to write import docx. The page of the docx project on PyPI shows "
        "version 0.2.4 as its latest release, dated 6 February 2014, still offering pip install docx; the study installed it in Python 3.14.6 and the import failed with "
        "ModuleNotFoundError: No module named 'exceptions', a module of Python 2, and this build ran that import again and got the same line. The working package, python-docx, was at version "
        "1.2.0, released on 16 June 2025.",
        "A .docx file is a ZIP of XML; install python-docx, then import docx.")

# ---- 18 reading paragraphs and runs ----------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithWord", "usecases", (0.5, 1.45, 3.9, 3.15), fs=8)
pn = "docxReadCut_v1_0_0.py"
a18, b18 = span(pn, "import docx")
f18 = bestfs(pn, (a18, b18), 4.9, 3.4)
p18, bot18 = prog(pn, 4.6, 1.55, pw(pn, (a18, b18), True, f18), fs=f18, lines=(a18, b18), show_out=True)
content("Reading paragraphs and runs", "A paragraph holds runs; tables, headers and hyperlink text are not in the runs",
        [dg, dcap, p18],
        "The use-case diagram lists what the chapter does with a Word document: read the paragraphs and runs, set the style of a paragraph, make a paragraph style, add headings, set "
        "the bold attribute of a run, add a page break and add a picture. The program reads back what it wrote. doc.paragraphs is a list of Paragraph objects in body order, and an "
        "empty paragraph counts. A paragraph is split into runs wherever the formatting changes: the three runs are Some , bold and text, with bold None, True, None. The chapter prints "
        "the third run of its demo paragraph as and some , where the shipped demo.docx has text and some , which is the one place the replay of the chapter's statements differed. doc.paragraphs "
        "holds only the body's own paragraphs, so the text of a table cell and of a section header has to be read from the cell and from the header. And for a paragraph that "
        "contains a hyperlink, text includes the linked words, before linked, in python-docx 1.2.0, but runs lists only the run before it: the linked text is in no Run, so a program "
        "that joins run texts loses it. The hyperlink here is built from a few lines of XML because python-docx 1.2.0 offers no call that writes one. A Run has a bold attribute with "
        "three states, which the writing slides come to.",
        "Read paragraphs for the body; tables, headers and link text need their own door.")

# ---- 19 the book's demo.docx -------------------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "shippedDemoDocxCut_v1_0_0.py"
a19, b19 = span(pn, "import docx")
c19, t19, bot = pair(pn, (a19, b19), 0.5, 1.55, 9.0, 2.7)
content("The book's demo.docx, restyled", "The chapter's restyling of its demo file: Quote Char on one run, underline on another",
        [c19, t19, foot("The title paragraph became Normal; the first run took the character style Quote Char; underline was set on the run bold. A run with no style of its own shows Default Paragraph Font. " + L_LIVE_DOCX + " " + hidden(pn, a19), 0.5, round(bot + 0.1, 2), 9.0, fs=9)],
        "The program opens the Word file the book ships, demo.docx, which it fetches from the online materials and checks against its sha256 before use, and lists its seven "
        "paragraphs with the name of their style: Title, Normal, Heading 1, Intense Quote, List Bullet, List Number and an empty Normal. The second paragraph holds four runs, "
        "A plain paragraph with some , bold, text and some and italic, with bold True only on the second and italic True only on the last. Then it does what the chapter does: the first "
        "paragraph takes the style Normal, the first run of the second takes the character style Quote Char, and the second run is underlined; the file is saved as restyled.docx "
        "and read back. The file itself says that its author is Cisco Employee and that it was last modified by Al Sweigart. The chapter's printout says the third run is and some ; the "
        "shipped file has text and some , and that is the only difference the replay found. Restyled.docx is a file the reader makes: the zip of the online materials does not "
        "hold it, nor helloworld.docx or encrypted.pdf. Microsoft Word itself was not available, so the statement that the style names in the Word Styles pane match the list "
        "the chapter prints is checked only against the template of python-docx.",
        "Give a run a character style and a paragraph a paragraph style.")

# ---- 20 styles -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ChoosingAStyle", "activity", (0.5, 1.4, 4.4, 3.2),
                   grid={"name": (1, 0), "exists": (1, 1), "make": (0, 1), "kind": (1, 2), "para": (1, 3), "run": (2, 2), "save": (1, 4)},
                   cols=[(0.0, 1.2), (1.45, 1.8), (3.52, 0.88)], rows_n=6, starts=(2, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "name"): "h", ("make", "para"): "vh", ("run", "save"): "vh"}, fs=8, nh=0.46, dh=0.5)
pn = "stylesCut_v1_0_0.py"
a20, b20 = span(pn, "doc = docx.Document()")
f20 = bestfs(pn, (a20, b20), 4.6, 3.4)
p20, bot20 = prog(pn, 5.0, 1.55, pw(pn, (a20, b20), True, f20), fs=f20, lines=(a20, b20), show_out=True)
content("Styles: an exact name and the right kind", "A paragraph takes a paragraph style, a run a character style, and the name must match",
        [dg, dcap, p20],
        "The workflow is the chapter's section on styling paragraph and run objects: choose the name of a style; if the template has no style with that exact name, make one with "
        "add_style(); then decide whether the style is for a whole paragraph, and assign it to the style of the paragraph or of the run; save the document. The transcript runs the two "
        "refusals. A paragraph accepts only paragraph styles and a run only character styles: paragraph.style = 'Quote Char' raises ValueError, assigned style is type CHARACTER (2), need type "
        "PARAGRAPH (1), and run.style = 'Quote' raises the reverse. A style name must match exactly: 'List Number ' with the trailing space the chapter prints raises KeyError, no style with "
        "name 'List Number ', while 'List Number' works. The chapter prints a list of 34 default style names. A new document has 164 styles of four kinds, 27 character, 1 list, 36 paragraph "
        "and 100 table, and the chapter's MacroText is the id of a style named macro, which python-docx 1.2.0 finds only through a lookup by id that is deprecated and warns. "
        "A custom paragraph style is made with styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH), whose base can be Normal and whose font can be set; the invitations "
        "program of slide 23 does it three times.",
        "Match the style name exactly, and give a paragraph a paragraph style.")

# ---- 21 writing: paragraphs, runs and bold -------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("BuildingAWordDocument", "sequence", (0.5, 1.45, 4.8, 3.15), fs=8, head_w=1.15)
pn = "writeRunsCut_v1_0_0.py"
a21, b21 = span(pn, "doc = docx.Document()")
f21 = bestfs(pn, (a21, b21), 4.1, 3.4)
p21, bot21 = prog(pn, 5.4, 1.55, max(3.9, pw(pn, (a21, b21), True, f21)), fs=f21, lines=(a21, b21), show_out=True)
content("Writing: paragraphs, runs and bold", "Each call returns the next object; bold has three states and strike is a font's",
        [dg, dcap, p21,
         card("Table 17-1 is mostly wrong", "Only 3 of 12 are on Run; the rest: run.font.",
              5.4, round(bot21 + 0.15, 2), 4.1, round(4.95 - bot21 - 0.15, 2), fs=9.5, accent="orange")],
        "The sequence diagram is the chapter's way of building a paragraph: the program calls add_paragraph with the text and gets back the new Paragraph, calls add_run on it and gets "
        "back the new Run, sets the bold attribute of the run, and saves the document. The transcript runs it. The type names are Paragraph and Run and the paragraph then holds 2 runs. "
        "Bold is tri-state, as the chapter says: True writes <w:b/>, False writes <w:b w:val=0/>, and None writes nothing and removes the choice. Table 17-1 lists twelve text "
        "attributes as attributes of a Run, and only three are: bold, italic and underline. The others, strike, double_strike, all_caps, small_caps, shadow, outline, rtl, imprint and "
        "emboss, exist on run.font. The transcript shows the consequence: run.strike = True raises nothing and changes nothing, font.strike stays None and the XML has no element, while "
        "run.font.strike = True works. The chapter's table therefore sends a reader to a silent failure. Underline takes the values of WD_UNDERLINE, and WD_UNDERLINE.DOUBLE wrote "
        "<w:u w:val=double/>.",
        "Set strike, caps and shadow through run.font, not on the run.")

# ---- 22 headings, breaks, pictures ----------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "breaksCut_v1_0_0.py"
a22, b22 = span(pn, "import docx")
c22, t22, bot = pair(pn, (a22, b22), 0.5, 1.55, 9.0, 3.3)
content("Headings, breaks and pictures", "Levels 0 to 9, a page break is a run, and a picture takes its height from its width",
        [c22, t22,
         card("Three counts in one chapter", "The chapter says heading levels run 0 to 4, then 1 to 9; add_heading accepts 0 to 9 and "
              "refuses 10. Level 0 is the Title style.", t22["x"], round(t22["y"] + t22["h"] + 0.15, 2), round(9.5 - t22["x"], 2),
              round(4.95 - (t22["y"] + t22["h"] + 0.15), 2), fs=9.5, accent="slate"),
         foot(hidden(pn, a22), 0.5, round(bot + 0.08, 2), 5.0, fs=9)],
        "Headings come from add_heading(text, level). The chapter gives the levels as 0 to 4 in one sentence and 1 to 9 in the next. The call accepts 0 to 9 and raises ValueError outside "
        "it, level must be in range 0-9, got 10, which is also the answer to practice question 12; level 0 is the Title style, level 1 is Heading 1 and level 9 is Heading 9. A page "
        "break is a run: add_run().add_break(WD_BREAK.PAGE) wrote <w:br w:type=page/>, and a newline in the text of add_run becomes a line break. A picture is added with add_picture(), "
        "which returns an inline shape whose size is in English Metric Units, 914,400 to the inch. A picture of 60 by 80 pixels with no width came out at 762,000 by 1,016,000, which is "
        "the pixels at 72 per inch, and with width=Inches(1) it came out 914,400 by 1,219,200, so the height follows from the width and keeps the picture's shape; giving both width and "
        "height can distort it. The same picture added twice was stored once in the file's word/media folder, and the file is a ZIP that begins with the bytes PK. The pictures here are "
        "made with Pillow, a small red PNG, because the chapter's zophie.png is not needed to show the sizes.",
        "A page break is a run, and a picture needs only a width.")

# ---- 23 Custom Invitations, and what was not run ----------------------------------------------------------------------------------------------------------------------------------------------
pn = "customInvitationsCut_v1_0_0.py"
a23, b23 = span(pn, "guests = [")
f23 = bestfs(pn, (a23, b23), 5.8, 3.4)
w23 = pw(pn, (a23, b23), True, f23)
p23, bot23 = prog(pn, 0.5, 1.55, w23, fs=f23, lines=(a23, b23), show_out=True)
x23 = round(0.5 + w23 + 0.25, 2)
content("Custom Invitations, and what was not run", "Styles made in code, one invitation per page, and a page count seen in LibreOffice",
        [p23,
         card("Styles made in code", "python-docx uses only styles that exist, so add_style() makes the three the invitation needs; "
              "the page break after each guest but the last leaves no blank page.", x23, 1.5, round(9.5 - x23, 2), 1.5, fs=9.5, accent="slate"),
         card("NOT EXECUTED here", "Microsoft Word and a PDF viewer were not run. LibreOffice 24.2 opened the Word files the research wrote and counted 5 pages for the "
              "5 invitations.", x23, 3.1, round(9.5 - x23, 2), 1.36, fs=9.5, accent="orange"),
         foot(hidden(pn, a23), x23, 4.5, round(9.5 - x23, 2), fs=8)],
        "The second practice program reads a list of guest names and writes a Word document with one invitation per page. Because python-docx can only use styles that exist, the chapter "
        "tells the reader to prepare them in a blank Word file; the study made them in code, with styles.add_style, so the program here makes Invite Lead, Invite Name and Invite Detail "
        "from Normal and sets their size and bold. Each guest gets five paragraphs and, except after the last guest, a page break: the transcript says 29 paragraphs, 4 page breaks for "
        "5 guests and lists the five names with the style Invite Name. The page break after each invitation but the last means that a viewer should show 5 pages, not 6. The "
        "research converted the Word files it wrote to PDF with LibreOffice 24.2 and counted 5 pages for the 5 guests, 2 pages for the file with a page break and 1 for the others, and "
        "saw the text; that is one observation in one program. Microsoft Word itself and a PDF viewer were NOT EXECUTED, and nothing on this slide is claimed about how they show the "
        "files. The same holds for the chapter's figures of the Styles pane, which are screenshots of Word.",
        "Make the styles in code, break after every guest but the last.", notexec=True)

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("PdfAndWordAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=1.6)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The PDF format comes first: a header, objects, a table and a trailer; text that is drawing commands in stream order; and text that a box "
        "does not remove. Reading PDFs follows: the pages of a PdfReader start at index 0, layout mode reads the page by its columns, and images are read from a page. Writing PDFs: a tuple is a "
        "page range, rotation adds up, and AES-256 needs a package. Word documents: a docx file is a ZIP archive of XML, a paragraph holds runs, and a style has an exact name. Writing Word "
        "documents: headings have levels 0 to 9, bold has three states, and a picture is added from a width. The last branch is tools and practice: install python-docx and import docx, "
        "Project 12 joins the pages, and a dictionary is tried in both cases. Together they answer the first question of the chapter, what a program can do with documents made for "
        "people, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 17 - free online", PUB["P01"][2]],
         ["pypdf documentation", PUB["P06"][2]],
         ["python-docx documentation", PUB["P26"][2]]]
_ref = [["pypdf: encryption and decryption", PUB["P11"][2]],
        ["pypdf: merging PDF files", PUB["P10"][2]],
        ["pypdf: post-processing of extracted text", PUB["P08"][2]],
        ["python-docx: working with styles", PUB["P22"][2]]]
_hist = [["John Warnock and Camelot (Wikipedia)", STORY["WarnockCamelot1991"]["link"]],
         ["ZIP, the file format (Wikipedia)", STORY["ZipFormat1989"]["link"]],
         ["Office Open XML (Wikipedia)", STORY["OoxmlStandard2006"]["link"]],
         ["PDF 1.7, ISO 32000-1 (Library of Congress)", STORY["PdfBecomesIso2008"]["link"]],
         ["History of pypdf: four names", STORY["PypdfFourNames"]["link"]],
         ["The docx package on PyPI (do not install)", STORY["DocxNameTrap2014"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every "
        "listing of the chapter; the documentation of pypdf and of python-docx describe the two packages. The reference links are the pages for the topics where the deck corrected the "
        "chapter: encryption, merging, the post-processing of extracted text and styles; the rest of the fifty-odd sources of the research, among them the PDF standard itself, the pages on "
        "images and watermarks, pdfminer.six and qpdf, are in the research package. The history links are the sources behind the six stories of the chapter. Two of them are slides, "
        "the Camelot memo of 1991 and the ZIP format of 1989; the other four were told in the notes: the Office Open XML standard, Ecma in 2006 and ISO in 2008, on the slide of the "
        "ZIP archive; the PDF standard ISO 32000-1 of July 2008 on the slide of the file structure; the four names of the library on the slide of what a program can do; and the "
        "package docx that cannot be imported on the slide of the ZIP archive.",
        "Textbook, package documentation and history, opened the day this deck was built.")

# ---- 26 closing ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A PDF stores drawing commands: text comes out in stream order, and a black box hides nothing.",
            "Pass pages= to merge(), ask for AES-256 by name, and read what decrypt() returns.",
            "A .docx file is a ZIP of XML: paragraphs hold runs, and bold has three states.",
            "A style needs its exact name and the right kind; strike belongs to run.font."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The console rows use only "
        "documents made in memory, so they can be typed into any Python that has pypdf, python-docx and Pillow; the programs build their own documents, and the two that read the "
        "book's files fetch them and check their hash first. The rows were run again under Python 3.14.6 with pypdf 6.20.1 and python-docx 1.2.0 each time the deck was built, and "
        "the programs were run again by the check that compares the slides with the recording. What was not run is marked on its slide: the language-model clean-up, Microsoft Word "
        "and a PDF viewer. The next chapter of the book works with CSV, JSON and XML files, where a program reads data that people and other programs wrote in plain text, and what this "
        "chapter taught about formats, optional packages and the difference between a file made to be read and a file made to be parsed carries over.",
        "Questions are welcome; bring a PDF or a Word file to open.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("A PDF and what a program can do", "What a program can do with a PDF", "Header, table and drawing commands"),
          ("Reading text and images", "Reading text, page by page", "Images, scans and the book's PDF"),
          ("Writing PDFs: pages, rotation, locks", "Copying pages: a tuple is a range", "Decrypt: the life of an encrypted PDF"),
          ("Projects with PDFs", "Project 12: combine many PDFs", "PDF Password Breaker, and its worst case"),
          ("Word documents: package, paragraphs, runs", "A .docx file is a ZIP of XML", "The book's demo.docx, restyled"),
          ("Styles and writing Word documents", "Styles: an exact name and the right kind", "Custom Invitations, and what was not run"),
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
S[1]["sub"] = "Seven parts; every range is a run of slides you can jump to"
S[1]["take"] = "Seven parts, from a PDF's bytes to a Word invitation."
S[1]["notes"] = ("The route has seven parts. It starts with the PDF: what a program can do with it, the memo that began the format, and the header, the table and the drawing "
                 "commands that a file holds. Then reading: text page by page, the language-model clean-up that was not run, and the images of the book's own PDF. Then writing PDFs: "
                 "copying pages, rotating and stamping them, and the encryption that is RC4 unless you ask for AES-256, with the life of an encrypted file. Then three projects with "
                 "PDFs: combining many files, PDF Paranoia and the Password Breaker with its worst case. Then Word: a .docx file is a ZIP of XML, paragraphs and runs, and the book's "
                 "demo file. The sixth part is styles and writing Word documents, ending with the invitations and with what was not run. The last part is a one-map summary and the "
                 "resources. The ranges name the exact slides, so you can return to the part you need. Two of the slides are true stories and four more are told in the notes; the eight "
                 "narrative diagrams of the chapter are drawn from the same specifications as the interactive page. Every output was printed by Python 3.14.6 with pypdf 6.20.1 and "
                 "python-docx 1.2.0, the programs that read the book's files say so, and what could not be run is marked on its slide.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
        if i.get("t") == "prog" and i.get("label"):
            import re as _re
            m = _re.search(r"program ([A-Za-z0-9_.]+)", i["label"])
            if m and PROGS[m.group(1)]["kind"] == "live":
                words = PROGS[m.group(1)]["livekey"]
                if not all(w in json.dumps(s["items"]) for w in words):
                    raise SystemExit("REFUSED: slide %r shows the LIVE program %s without saying so (%r)" % (s["title"], m.group(1), words))
if len(S) != 26:
    raise SystemExit("REFUSED: %d slides, the plan is 26" % len(S))
if set(SHOWN) != set(DIAG):
    raise SystemExit("REFUSED: diagrams not on a slide: %r" % (set(DIAG) - set(SHOWN)))
plan = {"meta": {"title": "Ch. 17: PDF and Word Documents", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "measured": MEASURED}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; measured", MEASURED)
