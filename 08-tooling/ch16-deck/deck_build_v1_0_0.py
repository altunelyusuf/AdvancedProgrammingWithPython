#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 16 (SQLite Databases) on the CME classroom standard.

Same regime as chapters 10 to 15: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources,
full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their
line numbers) with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6, whose sqlite3 module links SQLite 3.53.1); the
speaker notes are prose for the reader and carry only what the chapter's RDODI research package (03-materials/ch16/rdodi,
sen0414_ch16_rdodi_data_v1_0_2.py, findings F1 to F18), its records (08-tooling/ch16-page/*.json) or a program of this deck
established.

What this chapter adds against chapter 15: nothing here depends on a web service. Eleven of the fifteen recorded programs build their
own database, in memory or in a temporary folder; four read the book's own database sweigartcats.db, which they fetch from
nostarch.com on their first run and check against a sha256 beginning 41f0d0b5bc2e (they are LIVE, and every slide that shows one says
so, as honesty_check_v1_0_0.py requires). Three timings of the research record (the index, the place of the database, the number of
writers) are shown as single runs and say so. What could not be run - the three graphical applications, the Windows and macOS installers,
sudo apt install sqlite3 - is marked NOT EXECUTED on its slide. The eight narrative diagrams of the chapter
(sen0414_ch16_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py, with a five-state
diagram added) and checked by diagram_check_v1_0_0.py; one table (the storage classes) and one chart (the size of an index) are native
PowerPoint objects whose data the deck check computes again; no photograph is used, because no file could be fetched and licensed;
two of the six stories are slides (SQLite's beginning, Little Bobby Tables) and four are told in the notes.

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


ST = load("stories16", os.path.join(HERE, "..", "sen0414_ch16_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams16", os.path.join(HERE, "..", "sen0414_ch16_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi16", os.path.join(HERE, "..", "sen0414_ch16_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s, SQLite 3.53.1" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires the LIVE line on every slide that shows a LIVE program, and 'single run' on every
# slide that shows a measured time)
L_LIVE = "Shipped database: sweigartcats.db of the book's online materials, fetched from nostarch.com at run time, sha256 41f0d0b5bc2e... checked."
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
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states5, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap


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


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.85, 4.5, fs=10.5, cap=False)
S.append({"kind": "title", "title": "Chapter 16: SQLite Databases",
          "sub": "How a program keeps its data in one file: the sqlite3 module, tables and types, CRUD, transactions, keys and rowids",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made. The book's own database and the sqlite3 shell were fetched and hash-checked; what could not be run is marked on its slide.", 0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapters 14 and 15 worked on spreadsheets: a file that a program opens from its own disk, and a sheet that lives on Google's servers. "
                   "Chapter 16 turns to the tool that replaces both when the data has to be searched, changed by several statements at once and "
                   "kept consistent, a database, and to the one database that needs no server at all, SQLite. This deck follows the chapter in its "
                   "own order: what a database table is and how it differs from a spreadsheet; how a program connects to a file and creates a table "
                   "with types; the four operations of create, read, update and delete, with placeholders instead of pasted text; transactions "
                   "that keep or undo a group of changes; the structure of tables, with foreign keys and joins; and copies, tools and the two "
                   "practice programs. It adds what the chapter leaves out and what the research found when every printed output was run again: "
                   "the foreign key of the chapter's second table cannot be enforced, the dump of the book's own database fails from Python 3.13, "
                   "the number of data types is miscounted, a rowid can be handed out twice, and a database in memory is not the fast one. "
                   "Everything printed on these slides was produced by Python 3.14.6, installed with uv, whose sqlite3 module links SQLite 3.53.1, "
                   "and nothing needed a network except the two programs that fetch the book's database and check its hash.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV, "SQLite 3.53.1"]}],
        "The first question is the chapter's spine, and it is a question about words. INSERT, UPDATE and DELETE change a database; SELECT only "
        "reads it; CREATE TABLE, ALTER TABLE and DROP TABLE change its structure. What decides whether a change is kept, undone or refused is "
        "the transaction: a statement that breaks a rule, such as a NOT NULL column or a STRICT type, is refused and leaves nothing behind, "
        "a group of statements is kept by commit() and undone by rollback(), and the module itself has two ways of deciding when a "
        "transaction begins. The second question is the watch-out of the deck. The chapter is sound in outline, but when its 131 interactive "
        "statements were replayed on the book's own database, 103 printed what the page prints, 27 differed and one was a placeholder; and "
        "several claims do not hold for the module or the library of today: the foreign key of the second table cannot be enforced, the "
        "dump of the shipped file fails from Python 3.13, the count of six data types lists five, and the index does not serve the chapter's "
        "own LIKE queries. Each slide says where a printed line differs and on what evidence. The chips give the size of the chapter as this "
        "deck covers it: six branches, the topics beneath them, the console rows and the programs that were run, the eight diagrams, and the "
        "Python and SQLite releases that printed every result.",
        "Know what changes the data and what keeps it; then check what the book printed.")

# ---- 4 SQLite and what a program can do with it ---------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithSqlite", "usecases", (5.65, 1.45, 3.9, 3.15), fs=8)
c, bot = con("noserver", 0.5, 1.5, 5.0, fs=9, cap=False)
content("SQLite and what a program can do with it", "A library and one file: no server to start, no user to grant",
        [dg, dcap, c,
         card("A library, and a module", "Python ships sqlite3 since release 2.5 (2006); the SQLite inside is the build's: "
              "3.45.1, 3.50.4 or 3.53.1 on ten interpreters.", 0.5, round(bot + 0.15, 2), 5.0,
              round(4.95 - bot - 0.15, 2), fs=9.5, accent="slate")],
        "SQLite is not a server that a program talks to; it is a library that the program loads, and the database is one ordinary file. "
        "Because there is no server there are also no accounts to manage, and the console shows it: GRANT and CREATE USER are syntax errors. "
        "The same console shows how large such a file may grow. The default page is 4096 bytes and the default maximum is 4,294,967,294 pages, "
        "which is 17,592,186,036,224 bytes at that page size; at the largest page of 65,536 bytes the limit is 281,474,976,579,584 bytes, the "
        "281 terabytes that SQLite's page on limits gives. The module is part of the Python standard library since release 2.5 of 19 September "
        "2006, when the pysqlite wrapper was added under the name sqlite3. The library inside it belongs to the build, not to the "
        "language: the ten interpreters of the study, Python 3.11, 3.12, 3.13 and the seven releases 3.14.0 to 3.14.6, link SQLite 3.45.1, "
        "3.50.4 or 3.53.1, and sqlite.org offered release 3.54.0 on 12 October 2026. SQLite is in the public domain, its authors describe it "
        "as the most widely deployed database engine, and it is tested with simulated power loss. The use-case diagram lists what a program "
        "can do with one database through the module: insert rows, read them with a query, update and delete them, alter and drop tables, "
        "join tables through a foreign key, and back a database up or dump it as text. The rest of the deck takes these in the order of the chapter.",
        "SQLite is a library and a file, and the build chooses its version.")

# ---- 5 story: Hipp ------------------------------------------------------------------------------------------------------
content("SQLite began in 2000 on a Navy program", STORY["SqliteBegins2000"]["when"],
        [card("A database without a server", "D. Richard Hipp designed SQLite while working for General Dynamics on a US Navy contract: software for "
              "the damage-control system of guided-missile destroyers. The first release is dated 17 August 2000.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Spring 2000: designed for a Navy contract",
             "17 Aug 2000: first release",
             "A library and one file: no server to run",
             "Public domain: no licence to sign"]},
         factrow("SqliteBegins2000")],
        story_notes("SqliteBegins2000") + " Two of the facts on the slide were also read on SQLite's own pages: that the code is in the public domain, "
        "and that a database is a single file read and written through a library.",
        "A database can be a library and a file, not a server.")

# ---- 6 rows are tuples; the rowid ------------------------------------------------------------------------------------------
c, bot = con("table", 0.5, 1.5, 9.0, fs=9.5, cap=True)
content("Rows are tuples, and every row has a rowid", "To Python a table is a list of tuples; SQLite numbers each row itself",
        [c,
         {"t": "text", "x": 0.5, "y": round(bot + 0.05, 2), "w": 9.0, "h": round(4.97 - bot - 0.05, 2), "fs": 11, "color": "ink",
          "body": "fetchall() returns a list with one tuple per row and one item per column, in the order of CREATE TABLE. SELECT * leaves the "
                  "rowid out; naming it, or oid, or _rowid_, brings back the same number, here 1 for the first row."}],
        "The chapter sets a table against a spreadsheet: a row is a record, a column has a name and a type, and SQLite adds a column of its own, the "
        "rowid, a whole number that identifies the row. The console builds the chapter's cats table with the keyword STRICT, which the "
        "next slides explain, stores two cats and reads them back. What comes back is a list, and each item of the list is a tuple, the first being "
        "('Zophie', '2021-01-24', 'black', 5.6); that is the chapter's picture of a table as a list of tuples, and it holds. The rowid is hidden: "
        "SELECT * lists the four columns, SELECT rowid, * puts the rowid first, and rowid, oid and _rowid_ are three names for the same value. "
        "The helper do() runs a statement that returns no rows and prints nothing, and run() returns the rows of a statement, so the console prints "
        "only what matters; run it in any Python, because it uses a database in memory and the standard library alone. The chapter claims the "
        "rowid does not change when other rows are deleted, which is true of the rows that stay but not of the number itself; slide 19 shows "
        "when it is handed out again. The chapter's opening question, the cats between 3 and 5 kilograms born before October 2023, was also run "
        "on the book's database: the query and a Python loop over all 100 rows returned the same six cats.",
        "A table is a list of tuples, plus a hidden number for each row.")

# ---- 7 connect, create, close ---------------------------------------------------------------------------------------------------
dg, dcap = diagram("FromConnectToRows", "activity", (0.5, 1.45, 4.6, 3.15),
                   grid={"connect": (0, 0), "table": (0, 1), "insert": (0, 2), "changed": (0, 3), "read": (0, 4), "close": (0, 5), "commit": (1, 3)},
                   cols=[(0.0, 2.8), (3.25, 1.35)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "connect"): "h"}, fs=8, nh=0.4, dh=0.5)
c, bot = con("connect", 5.3, 1.5, 4.2, fs=9, cap=True)
content("From connect() to rows, and a closed file", "The steps of the chapter in order, and what a connection to memory shows",
        [dg, dcap, c,
         card("In memory is not the speed-up", "2,000 single inserts, one run: 0.002 s in memory, 2.236 s in a file, because each is a durable "
              "commit; in one transaction the file took 0.0025 s. Measured as a single run on 12 Oct 2026.", 5.3, round(bot + 0.12, 2), 4.2,
              round(4.95 - bot - 0.12, 2), fs=9, accent="orange")],
        "This is the chapter's own sequence of steps, drawn as a workflow: connect to a database file, create the table if it does not exist, "
        "insert the rows, commit if the statement changed the data, read the rows with fetchall, and close the connection. The console "
        "runs the ends of it on a database in memory. A connection starts outside a transaction, SELECT sqlite_version() returns the library's "
        "release, 3.53.1 here, and after close() any statement raises ProgrammingError: Cannot operate on a closed database. A few more facts "
        "come from the study. connect() creates the file at once but writes nothing: a new example.db was 0 bytes after connect and after a SELECT, "
        "and 8,192 bytes after the first CREATE TABLE. A text file connects without an error and fails at the first statement with file is not "
        "a database. A with block commits or rolls back but does not close the connection; closing() from contextlib does, and a connection that "
        "is simply dropped raises a ResourceWarning. The chapter says a database in memory is much faster than one in a file, and the card gives "
        "the measurement behind the correction. The numbers are one run on one machine on 12 October 2026 and vary with the machine, and what "
        "they show is that speed is decided by the commit, not by the place. Each connect(':memory:') is a separate database, so two "
        "connections to memory do not see each other's tables. The story of the module is short: Python 2.5, released on 19 September 2006, "
        "added the pysqlite wrapper to the standard library as sqlite3, which is why a program can open a database with no installation.",
        "A connection is the file; the commit, not the memory, sets the speed.", measured=True)

# ---- 8 types ----------------------------------------------------------------------------------------------------------------------
pn = "strictTypes_v1_0_0.py"
a8, b8 = span(pn, "conn = sqlite3.connect(':memory:'")
f8 = bestfs(pn, (a8, b8), 5.6, 3.4)
w8 = pw(pn, (a8, b8), True, f8)
p1, bot = prog(pn, 0.5, 1.55, w8, fs=f8, lines=(a8, b8), show_out=True)
content("STRICT, affinity and the six that are five", "A STRICT table refuses a wrong type; an ordinary table only has a preference",
        [p1,
         card("Six types? Count again", "The chapter says SQLite has six and lists five. STRICT accepts six type words (INT, INTEGER, REAL, "
              "TEXT, BLOB, ANY); the storage classes are five.", w8 + 0.65, 1.5, 9.5 - w8 - 0.65, 1.95, fs=9.5, accent="orange"),
         card("STRICT came in 3.37.0", "Released on 27 November 2021; BOOLEAN, DATE, VARCHAR, NUMERIC and FLOAT are refused in a STRICT table.",
              w8 + 0.65, 3.55, 9.5 - w8 - 0.65, 1.4, fs=9.5, accent="slate")],
        "The program makes two tables with an INTEGER column, one STRICT and one ordinary, and tries to insert five values into each: the text 'Hello', "
        "the real 3.5, the text '42', the real 42.0 and NULL. In the STRICT table 'Hello' and 3.5 are refused with IntegrityError, cannot store "
        "TEXT value in INTEGER column s.i, and cannot store REAL value in INTEGER column; '42' is converted to the integer 42, 42.0 is stored as 42, "
        "and NULL is stored. In the ordinary table all five go in, because the declared type is only an affinity, a preference: '42' became the integer "
        "42, 42.0 became 42, but 'Hello' stayed text and 3.5 stayed real, which typeof() shows. The last statement tries a column of type BOOLEAN in "
        "a STRICT table and gets OperationalError, unknown datatype for bad.a. The chapter's own count is off by one: it says that SQLite has six data "
        "types and lists five, and the five it lists are the storage classes NULL, INTEGER, REAL, TEXT and BLOB. A STRICT table accepts the six type "
        "words INT, INTEGER, REAL, TEXT, BLOB and ANY, and the names the chapter's lists use, such as BOOLEAN, DATE, VARCHAR, NUMERIC and FLOAT, are refused "
        "in a STRICT table and only have an affinity in an ordinary one. The chapter's claim that STRICT came with a SQLite version used by Python "
        "3.11 and later is right: the release log of SQLite 3.37.0 is dated 27 November 2021, and Python 3.11 was run with SQLite 3.45.1. The release "
        "log opens with STRICT tables as a prescriptive style of data type management for developers who prefer that kind of thing.",
        "Declare STRICT so a column's type is a rule, not a hint.")

# ---- 9 reading the schema ---------------------------------------------------------------------------------------------------------
pn = "firstSession_v1_0_0.py"
a9, b9 = span(pn, "conn = sqlite3.connect('example.db'")
f9 = bestfs(pn, (a9, b9), 9.0, 2.75)
p1, bot = prog(pn, 0.5, 1.55, pw(pn, (a9, b9), True, f9), fs=f9, lines=(a9, b9), show_out=True)
content("Reading the schema", "The chapter's first session: create a table, list the tables and read the columns back",
        [p1,
         foot("sqlite_schema lists every table and index with the SQL that made it; sqlite_master is the old name for the same rows. PRAGMA table_info "
              "returns cid, name, type, notnull, dflt_value and pk for each column. CREATE TABLE IF NOT EXISTS with another column list changes nothing: the first "
              "definition stays.", 0.5, round(bot + 0.1, 2), 9.0, fs=10)],
        "The first listing of the chapter runs from top to bottom without a surprise, and the transcript is what it printed. connect() with "
        "isolation_level=None opens the file example.db, which the chapter treats as autocommit; CREATE TABLE IF NOT EXISTS makes the STRICT table of cats; "
        "the query on sqlite_schema, where the type is a table, lists [('cats',)]; PRAGMA table_info(cats) returns one tuple for each column "
        "with the fields cid, name, type, notnull, dflt_value and pk, so the name column shows notnull 1; and the second CREATE TABLE IF NOT EXISTS, "
        "with a different column list, does nothing, because the table exists, so the stored SQL is still the first one. Without the words IF NOT EXISTS "
        "the same statement raises OperationalError, table cats already exists, for cats and for CATS alike, because table names are not case-sensitive. "
        "sqlite_schema lists tables, indexes and views in the order they were created, and sqlite_master returned the same rows under the name that "
        "older programs use. The default value of a text column comes back as SQL text with its quotes, so a default of x is shown as 'x'. Finally the "
        "program asks whether the file has a size above zero, which is True because the CREATE TABLE has written the first pages; the study measured "
        "8,192 bytes, two pages of 4,096 bytes, and the file was the only file left in the directory after the connection closed.",
        "The schema is data too: SQLite keeps it in sqlite_schema.")

# ---- 10 values, dates and booleans -------------------------------------------------------------------------------------------------
tb = EX["_tables"]["storageClasses"]["rows"]
tbl = {"t": "table", "x": 0.5, "y": 1.5, "w": 3.9, "colW": [1.0, 1.2, 1.7], "fs": 10, "rowH": 0.3, "rows": tb}
c, bot = con("values", 4.6, 1.5, 4.9, fs=9, cap=True)
content("Python values and the five storage classes", "What goes in, how SQLite stores it, and what comes back",
        [tbl, c,
         card("No boolean and no date type", "True is stored as 1; TRUE and FALSE are 1 and 0 in SQL. Dates are text, real or integer read "
              "by date functions: date('2035-02-30') gave 2035-03-02.", 0.5, 3.75, 4.5, 1.2, fs=9.5, accent="slate"),
         card("Only five Python types", "None, int, float, str and bytes are bound; a list is refused, and an int past 63 bits raises "
              "OverflowError.", 5.2, round(bot + 0.1, 2), 4.3, round(4.95 - bot - 0.1, 2), fs=9.5, accent="orange")],
        "The table is computed, not typed: for each Python value the program stores it in a column with no type, asks typeof() for the storage "
        "class SQLite chose and reads the value back to see which Python type returns. None becomes null and comes back as None, an int becomes "
        "integer, a float real, a str text and bytes a blob; True is stored as the integer 1 and comes back as an int, because SQLite has no "
        "boolean. The module binds exactly these five Python types and the boolean; a value of any other type is refused. The console shows two "
        "of the refusals: an int of 2 to the power 63 is too large for the 64 bits of an INTEGER and raises OverflowError, Python int too large "
        "to convert to SQLite INTEGER, and a list raises ProgrammingError, because the module cannot bind it. Dates have no type either. They "
        "are stored as text, as a real number or as an integer and read by the date functions, and the functions are forgiving in odd "
        "ways: date('31/10/2035') returns None, but date('2035-02-30') returns the invented date 2035-03-02. Python's default adapter for "
        "datetime.date objects is deprecated since Python 3.12 and warns under every interpreter from 3.12, so a program should write "
        "the text of the date itself. TRUE and FALSE are accepted in SQL and are 1 and 0.",
        "Booleans and dates are conventions you keep, not types SQLite checks.")

# ---- 11 CRUD ------------------------------------------------------------------------------------------------------------------------
pn = "crudCats_v1_0_0.py"
a11, b11 = span(pn, "print(conn.execute('SELECT rowid, name FROM cats")
f11 = bestfs(pn, (a11, b11), 9.0, 2.3)
w11 = pw(pn, (a11, b11), True, f11)
p1, bot = prog(pn, 0.5, 1.55, w11, fs=f11, lines=(a11, b11), show_out=True)
content("Create, read, update and delete", "Four statements, and what each gives back: rows, a count, RETURNING, a rowid",
        [p1,
         {"t": "boxes", "x": 0.5, "y": round(bot + 0.15, 2), "w": 9.0, "h": round(4.95 - bot - 0.15, 2), "cols": 3, "fs": 11.5, "subfs": 9.5, "accent": [],
          "items": [{"label": "UPDATE ... WHERE", "sub": "rowcount says how many rows changed: 2"},
                    {"label": "DELETE ... RETURNING", "sub": "returns the deleted row in the same call"},
                    {"label": "INSERT, then lastrowid", "sub": "the rowid of the new row: 5"}]}],
        "Before this excerpt the program builds the cats table in memory and inserts four cats with executemany, one call for four rows. The excerpt "
        "then shows each operation with its answer. SELECT with ORDER BY and LIMIT 2 returns the two heaviest cats as (rowid, name); UPDATE with a "
        "question mark placeholder adds 0.1 to every black cat, and cur.rowcount is 2; DELETE ... WHERE name = ? RETURNING rowid, name deletes Jacob and "
        "hands back [(3, 'Jacob')] in one call; an INSERT of a name alone stores NULL in the other columns and lastrowid is 5; a SELECT with LIKE "
        "and ORDER BY lists the names with an o; and the last line aggregates: 4 rows, 3 with a fur, an average weight of 6.27. Look at "
        "the long number in the transcript: Toby's weight is shown as 6.8999999999999995 and Zophie's as 5.699999999999999, because 0.1 cannot be "
        "written exactly in binary floating point and SQLite's REAL is a double, so a program should round what it shows. The study also found "
        "how rowcount behaves: an UPDATE by rowid changed one row, the same UPDATE by name changed two cats named Zophie, UPDATE with a true "
        "condition changed all rows, DELETE with no condition removed every row and left the empty table in place. executemany is not all or nothing: "
        "when the second row of a second batch broke NOT NULL, the row before it stayed.",
        "Every statement gives back something: rows, a count or a rowid.")

# ---- 12 placeholders: the sequence --------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AParameterisedQuery", "sequence", (0.5, 1.45, 4.4, 3.15), fs=8, head_w=1.3)
c, bot = con("inject", 5.05, 1.5, 4.45, fs=9, cap=True)
content("A placeholder keeps a value as data", "Statement and value travel apart: pasted text changes the query, a bound value cannot",
        [dg, dcap, c,
         foot("execute() refuses a second statement, so the comic's attack cannot drop a table through it; executescript() would run it.",
              5.05, round(bot + 0.05, 2), 4.45, fs=9.5)],
        "A query with a question mark is an exchange in a fixed order. The program calls execute() with the statement and, as a separate tuple, the "
        "value; the module sends the statement and binds the value as data; SQLite returns the rows that match the whole value, and the module hands "
        "back a cursor. The console runs the attack. The text x' OR '1'='1 pasted into the query with an f-string closes the quote early and "
        "adds a condition that is always true, so every row comes back (both rows here, all four in the program of the next slide); the same text bound as a parameter is compared as one name and matches "
        "none. The third statement is the comic's attack: execute() refuses a second statement after a semicolon with ProgrammingError, You can only "
        "execute one statement at a time, so the table survives; executescript() runs several statements and would not refuse. OWASP and MITRE "
        "name the weakness, CWE-89, and recommend parameterised queries. The chapter's example is sound and, if anything, understated: the strangers "
        "whose text reaches a query include a file, a form or a spreadsheet read by an earlier chapter. A placeholder can stand for a value only, "
        "never for a table or column name. Named placeholders use a colon and a dictionary, and the errors are specific: a list given for :fur raises "
        "ProgrammingError, because a named parameter needs a mapping, and a dictionary without the key says You did not supply a value for binding parameter. "
        "A bare string such as 'black' is read as a sequence of five values.",
        "Bind values with placeholders; never paste them into SQL.")

# ---- 13 story: Bobby Tables -----------------------------------------------------------------------------------------------------------------
t1 = transcript("placeholdersAndInjection_v1_0_0.py", 0.5, 3.7, 5.8, fs=7.0)
content("Little Bobby Tables, 2007", STORY["BobbyTables2007"]["when"],
        [card("The comic every course quotes", "xkcd number 327, 'Exploits of a Mom' by Randall Munroe: a school phones a mother about her son, "
              "whose name is text that closes a statement and drops the table of student records.", 0.5, 1.4, 4.5, 1.45, fs=10.5),
         {"t": "beats", "x": 5.3, "y": 1.4, "w": 4.2, "h": 1.45, "fs": 11, "items": [
             "10 Oct 2007: xkcd 327 is published",
             "The son's 'name' ends the statement",
             "The student table is dropped",
             "Her advice: sanitize the inputs"]},
         factrow("BobbyTables2007", y=2.98),
         t1,
         card("Bound, not pasted", "Too few values, a list for a named placeholder and a missing key are each a ProgrammingError.",
              6.45, 3.7, 3.05, 1.25, fs=9.5, accent="slate")],
        story_notes("BobbyTables2007") + " The transcript is the whole run of the chapter's injection program: four rows with the f-string, none with "
        "the placeholder, the refusal of the second statement, the table intact, and the three binding errors.",
        "Never paste text into SQL; the comic made the point in 2007.")

# ---- 14 NULL, quotes, LIKE ------------------------------------------------------------------------------------------------------------------------
c, bot = con("nulls", 0.5, 1.5, 5.2, fs=8, cap=False)
content("NULL, double quotes, LIKE and GLOB", "Four traps in a WHERE clause that run without an error",
        [c,
         card("NULL equals nothing", "fur = NULL found no row, != 'black' skipped Mandy, IS NULL found her.",
              5.9, 1.5, 3.6, 1.1, fs=9, accent="slate"),
         card("A double quote: a column?", "fur = \"fur\" compared the column with itself and matched every cat with a fur. "
              "Use single quotes.", 5.9, 2.7, 3.6, 1.15, fs=9, accent="orange"),
         card("LIKE: ASCII case only", "'a' LIKE 'A' is 1; GLOB is case-sensitive (0); 'É' LIKE 'é' is 0.",
              5.9, 3.95, 3.6, 1.0, fs=9, accent="slate")],
        "The chapter filters with WHERE, and four details decide whether the filter does what the author means. NULL is not equal to anything, including NULL: "
        "fur = NULL matches no row, fur != 'black' skips the cat with no fur, because comparing NULL with anything gives NULL, which is not true, "
        "and IS NULL finds it; count(*) counts four rows where count(fur) counts three. The chapter writes its text in double quotes, as in WHERE "
        "name LIKE \"Ja%\", and that works only because SQLite accepts a double-quoted word that matches no column as a string. The study showed the "
        "other face of it: fur = \"fur\" compared the column with itself and matched every row with a fur, and the compile options of the build list "
        "no setting for it, so the legacy behaviour is on; SQLite's page on quirks lists double-quoted string literals among its gotchas, and the "
        "compile-time options call it a misfeature that SQLITE_DQS=0 disables. Use single quotes for text. Finally LIKE is case-insensitive for ASCII "
        "characters only by default, so 'a' LIKE 'A' is 1 but 'É' LIKE 'é' is 0, while GLOB is case-sensitive and uses * and ?. SQLite also accepts both "
        "= and == and both <> and !=, and BETWEEN is inclusive.",
        "WHERE trusts you: NULL, double quotes and LIKE each have a trap.")

# ---- 15 indexes --------------------------------------------------------------------------------------------------------------------------------------
t1 = transcript("indexPlans_v1_0_0.py", 0.5, 1.8, 6.15, fs=7.0, label="transcript of program indexPlans_v1_0_0.py", aligned=True)
ch = EX["_charts"]["indexSize"]
chart = {"t": "chart", "ctype": "bar", "x": 6.8, "y": 1.45, "w": 2.7, "h": 2.35, "labels": ch["labels"],
         "title": "10,000 rows, KiB", "series": [{"name": "KiB", "data": ch["values"]}], "dataLabels": True, "dlFs": 9}
content("An index serves some searches, not all", "SEARCH uses the index, SCAN reads every row; LIKE scans, GLOB and a range search",
        [t1, chart,
         card("What an index costs", "On 300,000 rows one search by indexed name took 0.0033 ms against 10.27 ms for a scan (3,087 times); 300,000 inserts "
              "took 4.7 times as long with two indexes (0.56 s against 0.12 s). Single runs on 12 Oct 2026; they vary with the machine.",
              0.5, 3.35, 6.15, 1.6, fs=10, accent="orange"),
         foot("The chart is computed: the size of the same 10,000 rows with no index, one and two.", 6.8, 3.85, 2.7, fs=8.5)],
        "The program builds a table of 1,000 cats, creates an index on the name and asks EXPLAIN QUERY PLAN for six searches. The plan says SEARCH ... "
        "USING INDEX idx_name for name = 'Cat0042', for name GLOB 'Cat00*' and for the range name >= 'Cat00' AND name < 'Cat01', and SCAN cats, a "
        "read of every row, for name LIKE 'Cat00%', for name LIKE '%42' and for fur = 'black', which has no index. LIKE does not use the index "
        "because the default index uses the BINARY collation and LIKE is case-insensitive, so the chapter's own LIKE queries would not use the "
        "index it builds; a leading wildcard could not use any ordinary index anyway. The last line counts the 100 names LIKE finds. An index is not free, "
        "and the chart shows the first price: the same 10,000 rows take 216 KiB in 54 pages of 4,096 bytes, 380 KiB with an index on the name and 512 KiB "
        "with a second index, each number computed again when the deck is checked. The card gives the other prices, in time, from the research "
        "record: a search by indexed name on 300,000 rows took 0.0033 ms against 10.27 ms for a scan, and 300,000 inserts took 4.7 times as long with two "
        "indexes. These are single runs on one machine and are not repeated by any check of the deck; the query plans and the sizes are.",
        "An index makes a search fast and every write slower.", measured=True)

# ---- 16 transactions: the workflow ---------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ATransactionEnds", "activity", (0.5, 1.45, 4.4, 3.15),
                   grid={"begin": (0, 0), "change": (0, 1), "ok": (0, 2), "commit": (0, 3), "rollback": (1, 2)},
                   cols=[(0.0, 2.5), (2.85, 1.55)], rows_n=4, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 3},
                   routes={("start", "begin"): "h"}, fs=8, nh=0.46, dh=0.58)
c, bot = con("txn", 5.1, 1.5, 4.4, fs=8.5, cap=False)
content("Begin, then commit or roll back", "A transaction keeps all its changes or none; a failed statement leaves nothing behind",
        [dg, dcap, c],
        "The workflow is the chapter's section on rolling back transactions. BEGIN starts a transaction, the statements change the data, and one choice "
        "ends it: if every statement succeeded, commit() keeps the changes, and otherwise rollback() undoes them. The console runs it with "
        "isolation_level=None, the chapter's switch for autocommit, so nothing is inside a transaction until BEGIN. After BEGIN and one INSERT, "
        "in_transaction is True; rollback() leaves count(*) at 0; a second BEGIN with an INSERT and commit() keeps one row; and one INSERT of three "
        "rows, the last with NULL in a NOT NULL column, is refused as a whole, with IntegrityError, and the count is still 1, because a single "
        "statement is atomic. The study also found that DDL is part of a transaction: a CREATE TABLE and a DROP TABLE inside BEGIN were undone by "
        "rollback(), and a rollback() after a lone INSERT in this mode undid nothing, because the INSERT had already been committed. The ACID "
        "properties, atomicity, consistency, isolation and durability, were named by Theo Haerder and Andreas Reuter in their 1983 paper, "
        "Principles of Transaction-Oriented Database Recovery, in ACM Computing Surveys, building on earlier work of researchers including Jim Gray. "
        "SQLite's own pages describe it as transactional and test it with simulated power loss. In the study an open transaction was invisible to "
        "a second connection until commit(), and a committed row survived closing and reopening while an uncommitted one did not. Another feature is that "
        "executescript() commits any pending transaction first.",
        "A transaction is all of its changes or none.")

# ---- 17 three modes ---------------------------------------------------------------------------------------------------------------------------------------------------
pn = "transactions_v1_0_0.py"
a17, b17 = span(pn, "conn = sqlite3.connect(':memory:', isolation_level=None)")
f17 = bestfs(pn, (a17, b17), 9.0, 3.0)
w17 = pw(pn, (a17, b17), True, f17)
p1, bot = prog(pn, 0.5, 1.55, w17, fs=f17, lines=(a17, b17), show_out=True)
content("Three ways to begin a transaction", "The default, autocommit=False and autocommit=True answer rollback() differently",
        [p1,
         foot("The first three lines of the transcript come from a loop over the three modes (lines 3 to 12, not shown). Python 3.12 added the autocommit "
              "attribute, absent on 3.11.17; with autocommit=True a rollback() left the row. A with block commits or rolls back and does not close.",
              0.5, round(bot + 0.05, 2), 9.0, fs=8.5)],
        "The module has two models of transaction control, and the transcript shows both. The first three lines come from a loop that opens a "
        "connection three times, with the default mode, with autocommit=False and with autocommit=True, creates a table, commits, inserts a row and "
        "calls rollback(). In the default mode, the legacy one, in_transaction is True after the INSERT but would stay False after a CREATE TABLE, "
        "and rollback() removes the row; with autocommit=False the module opens a transaction itself, rollback() removes the row and a new transaction "
        "opens at once; with autocommit=True the INSERT is committed immediately, in_transaction is False and rollback() leaves the row. The "
        "autocommit attribute exists from Python 3.12 on, it was absent on 3.11.17 and the 3.14 documentation calls autocommit=False the recommended value, "
        "so the chapter's isolation_level=None is the older switch. The excerpt then shows the context manager: a with block commits when it ends and "
        "rolls back when it raises, so the block that inserted 1 and then NULL left no rows, the transcript says NOT NULL constraint failed: t.a "
        "and rows after the failed block: 0. Finally one statement that inserts three rows, the last with NULL, is atomic and leaves none. In "
        "autocommit=False mode, execute('BEGIN') fails with cannot start a transaction within a transaction, because the module has opened one.",
        "Know which mode you are in before you trust rollback().")

# ---- 18 two writers -------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("TwoWritersOneFile", "sequence", (0.5, 1.45, 5.0, 3.15), fs=8, head_w=1.45)
t1 = transcript("twoWriters_v1_0_0.py", 5.7, 1.5, 3.8, fs=7.0)
content("Two writers, one file", "One writer holds the lock, the other is told it is locked; WAL lets readers in",
        [dg, dcap, t1,
         card("1,000 writers, one file", "5,000 rows stored, no error: 52.6 s with the rollback journal, 4.24 s with WAL (100 writers: 1.80 s and 0.83 s). "
              "Single run on one machine, 12 Oct 2026: the limit is throughput, not correctness.", 5.7, round(1.5 + t1["h"] + 0.15, 2), 3.8,
              round(4.95 - (1.5 + t1["h"] + 0.15), 2), fs=9, accent="orange")],
        "The chapter warns that SQLite is not the right choice for hundreds or thousands of simultaneous write operations, and the program tries the "
        "smallest case of it. Two connections open the same file with timeout 0. The first runs BEGIN IMMEDIATE and an INSERT and holds the write lock; "
        "the second asks to write at the same time and is answered with OperationalError, database is locked; in the default journal mode, delete, a "
        "reader sees 0 rows; the first commits and releases the lock. Then PRAGMA journal_mode = WAL switches the database to write-ahead logging, "
        "the first connection opens a write again and the second reads the committed count, 1, without being blocked; after the commit it reads 2. The "
        "directory then holds shared.db, shared.db-shm and shared.db-wal, and after both connections close only shared.db remains. The module's "
        "default busy timeout is 5 seconds, so a writer waits for the lock rather than failing at once, and only a writer that waits longer gets the "
        "error. The research tried the chapter's warning with 100 and then 1,000 operating-system processes that each inserted 5 rows into one file: "
        "nothing was lost, and the cost showed in time, so the limit is throughput and not correctness. Both numbers on the slide are one run on "
        "one machine on 12 October 2026 and vary with the machine.",
        "Many writers do not lose data in SQLite; they wait.", measured=True)

# ---- 19 the rowid through its life ------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ARowidThroughItsLife", "states", (0.5, 1.3, 9.0, 1.95), fs=8.5,
                   pos={"none": (0, 0), "assigned": (1, 0), "deleted": (2, 0), "renumbered": (0, 1), "reused": (2, 1)},
                   ways={("none", "assigned"): "h", ("assigned", "deleted"): "h", ("deleted", "reused"): "v",
                         ("assigned", "renumbered"): "down-left", ("reused", "assigned"): "left-up"})
t1 = transcript("rowids_v1_0_0.py", 0.5, 3.85, 3.3, fs=7.0)
content("The rowid is not a promise", "The largest rowid is handed out again; VACUUM renumbers a table without a key",
        [dg, dcap, t1,
         card("INTEGER PRIMARY KEY keeps it", "A column declared INTEGER PRIMARY KEY is an alias of the rowid and keeps its value through "
              "VACUUM; AUTOINCREMENT never hands out a number twice, at the price of the sqlite_sequence table.", 4.0, 3.65, 5.5, 1.3, fs=10, accent="slate")],
        "The chapter says that the rowid does not change when other rows are deleted, and the state diagram follows one rowid to show where the sentence "
        "is too strong. A row is inserted and receives the next rowid. If the row is deleted and it was the one with the largest rowid, the next insert "
        "receives that same number again, 4 and then 5 on the table with AUTOINCREMENT in the transcript, where a plain table gave 4 twice. A table with no "
        "INTEGER PRIMARY KEY can have its rowids renumbered by VACUUM: after deleting rows 1 and 2 of four, the rows (3, 'c') and (4, 'e') became "
        "(1, 'c') and (2, 'e'). A column declared INTEGER PRIMARY KEY is an alias for the rowid and keeps its values through VACUUM, and with "
        "AUTOINCREMENT a deleted number is never handed out again, which costs the table sqlite_sequence, the only name beginning with sqlite_ in the "
        "last line of the transcript. Why this matters comes two slides on: the chapter's foreign key points at the rowid, the very number VACUUM may "
        "change. The first row and the transitions all come from the chapter's paragraph on the rowid and from SQLite's pages on rowid tables, VACUUM and "
        "AUTOINCREMENT, which the research read and ran.",
        "Use an INTEGER PRIMARY KEY if a number must keep its meaning.")

# ---- 20 foreign key that works, join ---------------------------------------------------------------------------------------------------------------------------------------------
pn = "matchingMealIngredients_v1_0_0.py"
a20, b20 = span(pn, "conn.execute('CREATE TABLE ingredients", "' STRICT')")
f20 = bestfs(pn, (a20, b20), 5.1, 1.1, out=False, hi=8.0)
p0, bot0 = prog(pn, 0.5, 1.55, 5.1, fs=f20, lines=(a20, b20), show_out=False)
a20c, b20c = span(pn, "try:", "print(conn.execute('PRAGMA foreign_key_check')")
f20c = bestfs(pn, (a20c, b20c), 5.1, 4.95 - round(bot0 + 0.45, 2), hi=8.0)
p1, bot = prog(pn, 0.5, round(bot0 + 0.45, 2), 5.1, fs=f20c, lines=(a20c, b20c), show_out=True)
content("A foreign key that works, and a join", "The second practice program: meals and ingredients linked by a real key",
        [p0, p1,
         card("Switch it on, per connection", "PRAGMA foreign_keys = ON; the parent key is an INTEGER PRIMARY KEY. An orphan row is refused with "
              "FOREIGN KEY constraint failed, and foreign_key_check lists none.", 5.8, 1.5, 3.7, 1.75, fs=9.5, accent="slate"),
         card("Joined and grouped", "JOIN reads the two tables together, group_concat(...) joins the ingredients of each meal, and NOT IN finds "
              "the meals without butter.", 5.8, 3.35, 3.7, 1.55, fs=9.5, accent="orange")],
        "This is the second practice program of the chapter, the meal ingredients database, made so that it works. The book specifies a table of meals with a "
        "name and a foreign key REFERENCES meals (rowid); as printed, the first INSERT into ingredients fails with foreign key mismatch, so the program here "
        "gives the parent table an id INTEGER PRIMARY KEY and references meals (id), and switches enforcement on with PRAGMA foreign_keys = ON, which is "
        "off by default and per connection. The first excerpt is the two CREATE TABLE statements, the second the checks: the join returns ('Pancakes', "
        "'flour, milk, egg', 600.0) and ('Omelette', 'egg, butter', 170.0); an ingredient for meal 99 is refused with FOREIGN KEY constraint failed; "
        "PRAGMA foreign_key_check lists no orphans; and the meals that have no butter are [('Pancakes',)]. The program shown is the deck's copy of the "
        "corpus program with its SQL cut into pieces that fit a slide, and a check of the build requires that it print exactly what the corpus original prints. "
        "The idea behind the two tables is old. In June 1970 Edgar F. Codd, a mathematician at IBM's San Jose Research Lab, published A Relational Model of "
        "Data for Large Shared Data Banks in Communications of the ACM, volume 13, number 6; IBM's history page tells how, before it, getting data out of "
        "the large information systems of the 1960s took specialists who often wrote whole programs to reach one fact. A table for each kind of fact, linked by "
        "a number and read back with a join, is the relational model in a few lines.",
        "Put each kind of fact in its own table and join them.")

# ---- 21 shipped database ---------------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "shippedDatabaseCut_v1_0_0.py"
a21, b21 = span(pn, "conn.execute('PRAGMA foreign_keys = ON')", "print(conn.execute('PRAGMA integrity_check')")
f21 = bestfs(pn, (a21, b21), 7.4, 2.95)
w21 = pw(pn, (a21, b21), True, f21)
p1, bot = prog(pn, 0.5, 1.55, w21, fs=f21, lines=(a21, b21), show_out=True)
content("The book's foreign key cannot be enforced", "REFERENCES cats(rowid) names no real column; dumping the file fails from Python 3.13",
        [p1,
         {"t": "stat", "x": round(w21 + 0.7, 2), "y": 1.5, "w": round(9.5 - w21 - 0.7, 2), "h": 2.95, "vert": True, "items": [
             {"n": "100", "label": "cats in the file"}, {"n": "291", "label": "vaccinations"}, {"n": "24,576", "label": "bytes, 6 pages"}]},
         foot(L_LIVE + " Rows, bytes and the schema as the file holds them.", 0.5, round(bot + 0.08, 2), 9.0, fs=9)],
        "The shipped database holds the cats table without a primary key and the vaccinations table with FOREIGN KEY(cat_id) REFERENCES cats(rowid), "
        "and that declaration cannot be enforced. SQLite's page on foreign keys requires the parent key to be the primary key or a column with a UNIQUE index, and "
        "rowid is neither unless it is an alias, so with PRAGMA foreign_keys = ON every INSERT into vaccinations fails with OperationalError, foreign key mismatch - "
        "'vaccinations' referencing 'cats', exactly as the transcript shows; it is off by default, which is why the book's examples seem to work. The "
        "identical result came from Python 3.14.0 to 3.14.6, 3.13 and 3.12, and from SQLite 3.45.1, 3.50.4 and 3.53.1. A table rebuilt with id INTEGER "
        "PRIMARY KEY and REFERENCES cats(id) enforced the constraint and reported the orphan with PRAGMA foreign_key_check. The chapter's join works because "
        "a join does not need the constraint. The second finding follows from the first: Connection.iterdump() runs PRAGMA foreign_key_check first from Python "
        "3.13, so on this file it raises the same OperationalError, while Python 3.12 and 3.11 return 395 lines of the same file. The file is the one "
        "the program fetches from the online materials of the third edition, 24,576 bytes with 4,096-byte pages, passing integrity_check, with 100 cats and "
        "291 vaccinations; the zip also ships it a second time as sweigartcats-original.db, byte for byte equal. The deck's program is the corpus program with "
        "its long printed line cut in two.",
        "A key to the rowid cannot be enforced; give the parent a real key.")

# ---- 22 copying a database ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ChoosingHowToCopy", "activity", (0.5, 1.4, 5.05, 3.2),
                   grid={"open": (0, 0), "kind": (0, 1), "backup": (0, 2), "done": (0, 3), "dump": (1, 1), "check": (1, 2), "fix": (2, 2)},
                   cols=[(0.0, 1.7), (2.15, 1.4), (3.95, 1.1)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 4},
                   routes={("start", "open"): "h"}, fs=8, nh=0.5, dh=0.56)
t1 = transcript("backupAndDump_v1_0_0.py", 5.65, 1.55, 3.85, fs=7.0)
content("Copy a database: backup() or iterdump()", "A database copy goes through backup(); the SQL text of one goes through iterdump()",
        [dg, dcap, t1,
         card("Two copies, one catch", "backup(target) copies pages into another connection, even from memory to a file; iterdump() yields the SQL text. "
              "On the shipped file the dump fails from Python 3.13.", 5.65, round(1.55 + t1["h"] + 0.15, 2), 3.85,
              round(4.95 - (1.55 + t1["h"] + 0.15), 2), fs=9.5, accent="orange")],
        "The workflow has one real choice: is the copy to be a database or a text of SQL statements? A database copy is made with backup(), which copies the "
        "pages of one connection into another, and the program saves a database held in memory to the file copy.db, which then holds both rows in 8,192 "
        "bytes; backing up a connection onto itself raises ValueError, target cannot be the same connection instance. A text copy is made with iterdump(), "
        "which yields the statements of a database one at a time, and the transcript lists them: BEGIN TRANSACTION, the CREATE TABLE, one INSERT for each row, "
        "with the table name in double quotes, and COMMIT. Running them with executescript in an empty database rebuilt identical rows, and filter='cats' "
        "leaves out the index line. In the study backup() with pages=1 called its progress function several times and ended with status 101, SQLITE_DONE. The "
        "decision on the second branch is the finding of the research: on the book's own file iterdump() raises OperationalError, foreign key mismatch, from "
        "Python 3.13, because it runs PRAGMA foreign_key_check first, so the repair is to give the cats table a real key and dump again. The sqlite3 shell "
        "of release 3.54.0 has its own .dump command; the study ran it on a script and its dump began with PRAGMA foreign_keys=OFF.",
        "backup() copies a database; iterdump() copies its text.")

# ---- 23 practice 1 and the tools -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "catCheckerCut_v1_0_0.py"
a23, b23 = span(pn, "print(q('SELECT count(*) FROM cats')[0][0]", "print(q('SELECT name, count(*) FROM cats GROUP BY name")
f23 = bestfs(pn, (a23, b23), 5.9, 3.25)
w23 = pw(pn, (a23, b23), True, f23)
p1, bot = prog(pn, 0.5, 1.55, w23, fs=f23, lines=(a23, b23), show_out=True)
x23 = round(w23 + 0.7, 2)
content("The first practice program, and the tools", "Cat Vaccination Checker on the book's own file; the shell and three apps",
        [p1,
         card("The shell, and Python's own", "The official sqlite3 shell, release 3.54.0, ran a script and boxed its tables in a terminal. python -m sqlite3 "
              "example.db opens a second shell with no install.", x23, 1.45, round(9.5 - x23, 2), 1.45, fs=9, accent="slate"),
         card("NOT EXECUTED here", "DB Browser for SQLite, Letos (once SQLiteStudio), DBeaver, sudo apt install sqlite3 and the Windows "
              "and macOS installers were not run.", x23, 2.98, round(9.5 - x23, 2), 1.3, fs=9, accent="orange"),
         foot(L_LIVE, x23, 4.3, round(9.5 - x23, 2), fs=8.5)],
        "The first practice program of the chapter walks the book's own database and looks for the planted errors. The query joins vaccinations to cats and "
        "finds three vaccinations dated before the cat was born: Ruby, Java and Rocket, each with FVRCP and a date from 2001 to 2004 against a birth in "
        "2013 to 2023. A second query, with a LEFT JOIN and a count of distinct vaccines, finds seven cats that lack at least one of the three vaccines, "
        "rabies, FeLV and FVRCP: Molly, Sage, Hugh, Chester, Snowflake, Luke and Muffin, none lacking all three. There are 97 vaccinations of each vaccine, "
        "no orphan rows, and two cats named Tiger, so the name cannot identify a cat. The program is the deck's copy of the corpus program, with the long queries "
        "cut and one result printed per line. The tools were checked in part. The sqlite3 shell of release 3.54.0 was downloaded from sqlite.org, its SHA3-256 "
        "checked against the download page, and run on a script and in a terminal, where it prints a boxed table and the prompt SQLite-3.54 example.db-> where "
        "the book shows the list mode. python -m sqlite3 is a second shell inside Python. The page of SQLiteStudio now answers with a redirect to a page "
        "titled Letos, and DB Browser for SQLite and DBeaver Community answered 200. The three applications were not installed, and the installers and sudo apt "
        "install sqlite3 were not run, so nothing on this slide is claimed about how they behave.",
        "Run the checker on the book's file; the tools differ from the book.", notexec=True)

# ---- 24 summary: the mind map ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("SqliteDatabasesAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.35), fs=9, root_w=1.6)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The idea of a database comes first: a table is like a spreadsheet with a rowid, SQLite is one file with no server, "
        "and a query replaces a loop over a list. Connection and schema follow: connect() opens or creates the file, a STRICT table checks the types and the "
        "schema is read from sqlite_schema. CRUD operations are the largest branch: insert, update and delete change the rows, a placeholder keeps a value as "
        "data and an index speeds up a search. Transactions keep or undo changes, and a failed statement changes nothing; write-ahead logging helps "
        "several writers. Table structure covers alter and drop, the foreign key that links two tables and the join that reads them together. The last "
        "branch is copies, tools and practice: backup() and iterdump() copy a database, the sqlite3 shell and three graphical applications, and two practice programs "
        "use the shipped file. Together they answer the first question of the chapter, which statements change the database and what keeps the change, and the slides "
        "that say where a printed line differs answer the second.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 16 - free online", PUB["P01"][2]],
         ["sqlite3 in the Python 3.14 documentation", PUB["P06"][2]],
         ["Practical SQL, 2nd edition (the book to read next)", PUB["P05"][2]]]
_ref = [["STRICT tables", PUB["P09"][2]],
        ["SQLite foreign key support", PUB["P11"][2]],
        ["Transactions: BEGIN, COMMIT, ROLLBACK", PUB["P15"][2]],
        ["Write-ahead logging", PUB["P20"][2]]]
_hist = [["SQLite and D. Richard Hipp (Wikipedia)", STORY["SqliteBegins2000"]["link"]],
         ["IBM: the relational database, after Codd", STORY["CoddRelationalModel1970"]["link"]],
         ["What's new in Python 2.5: sqlite3 arrives", STORY["PythonGainsSqlite2006"]["link"]],
         ["xkcd 327, Exploits of a Mom", STORY["BobbyTables2007"]["link"]],
         ["SQLite 3.37.0 release log: STRICT tables", STORY["StrictTables2021"]["link"]],
         ["ACID (Wikipedia)", STORY["AcidNamed1983"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read "
        "online and holds every listing of the chapter, the Python documentation describes the sqlite3 module of release 3.14, and Practical SQL by Anthony DeBarros "
        "is the book the chapter points to for further SQL. The reference links are SQLite's own pages for the topics where the deck corrected the chapter: STRICT tables, "
        "foreign keys, transactions and write-ahead logging; the rest of the sixty-odd sources of the research, among them the pages on rowid tables, on VACUUM, on "
        "the query optimizer and on locking, are in the research package. The history links are the sources behind the six stories of the chapter. Two of them are "
        "slides, the beginning of SQLite and Little Bobby Tables; the other four were told in the notes: Codd's paper of 1970 on the slide of the meal ingredients, "
        "the arrival of sqlite3 in Python 2.5 on the slide of the connection, the strict mode of SQLite 3.37.0 on the slide of the types, and the name ACID of 1983 on "
        "the slide of the transaction.",
        "Textbook, SQLite's pages and history, opened the day this deck was built.")

# ---- 26 closing --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A value goes in with a placeholder, and a statement is all or nothing.",
            "STRICT makes a type a rule; the rowid is a number SQLite may hand out again.",
            "A key must name a real column: the book's rowid key cannot be enforced.",
            "In memory is not the fast part; the commit is, and many writers wait."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The "
        "console rows use only the standard library and a database in memory, so they can be typed into any Python, including one in a browser; the programs that "
        "build their own database need nothing else, and the two that read the book's file fetch it and check its hash first. The rows were run again under "
        "Python 3.14.6 with SQLite 3.53.1 each time the deck was built, and the programs were run again by the check that compares the slides with the recording. "
        "The next chapter of the book works with PDF and Word documents, where a program reads and writes files that other people made, and what this chapter "
        "taught about rows, types, keys and the cost of every commit carries over to any data that has to be kept in one place and kept correct.",
        "Questions are welcome; bring a database to open.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The idea of a database", "SQLite and what a program can do with it", "Rows are tuples, and every row has a rowid"),
          ("Connection, types and schema", "From connect() to rows, and a closed file", "Python values and the five storage classes"),
          ("CRUD, parameters and indexes", "Create, read, update and delete", "An index serves some searches, not all"),
          ("Transactions and writers", "Begin, then commit or roll back", "Two writers, one file"),
          ("Keys, rowids and joins", "The rowid is not a promise", "The book's foreign key cannot be enforced"),
          ("Copies, practice and tools", "Copy a database: backup() or iterdump()", "The first practice program, and the tools"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_parts[1] = ("Connection, types and schema", "From connect() to rows, and a closed file", "Python values and the five storage classes")
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
S[1]["take"] = "Seven parts, from one file to a copy of it."
S[1]["notes"] = ("The route has seven parts. It starts with the idea of a database, what a program can do with SQLite, the beginning of SQLite and the "
                 "way a table is a list of tuples with a hidden rowid, then the connection, the types, the schema and the values that go in, then the "
                 "four operations with placeholders, the traps of a WHERE clause and the index, then transactions and the two writers of one file, then "
                 "the rowid, the foreign key that works and the one in the book that cannot be enforced, then copies, the first practice program and the "
                 "tools, ending with a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Two of "
                 "the slides are true stories and four more are told in the notes; the eight narrative diagrams of the chapter are drawn from the same "
                 "specifications as the interactive page. Every output was printed by Python 3.14.6 with SQLite 3.53.1, the programs that read the book's "
                 "database say so, and what could not be run is marked on its slide.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
        if i.get("t") == "prog" and i.get("label"):
            import re as _re
            m = _re.search(r"program ([A-Za-z0-9_.]+)", i["label"])
            if m and PROGS[m.group(1)]["kind"] == "live" and L_LIVE not in json.dumps(s["items"]):
                raise SystemExit("REFUSED: slide %r shows the LIVE program %s without saying so" % (s["title"], m.group(1)))
if len(S) != 26:
    raise SystemExit("REFUSED: %d slides, the plan is 26" % len(S))
if set(SHOWN) != set(DIAG):
    raise SystemExit("REFUSED: diagrams not on a slide: %r" % (set(DIAG) - set(SHOWN)))
plan = {"meta": {"title": "Chapter 16: SQLite Databases", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "measured": MEASURED}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; measured", MEASURED)
