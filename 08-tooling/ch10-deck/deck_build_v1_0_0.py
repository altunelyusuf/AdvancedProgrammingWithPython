#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 10 (Reading and Writing Files) on the CME classroom standard.

Same regime as chapter 9: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows (no photographs this chapter either - Wikimedia
Commons was still 429-rate-limited from this session's egress IP when retried on 2026-10-11), consoles and whole
programs with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py); the speaker notes are prose for the reader.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories4110", os.path.join(HERE, "..", "sen0414_ch10_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
PD = sorted(__import__("glob").glob(os.path.join(HERE, "..", "ch10-page", "page_data_v*.json")),
            key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = {n["id"]: n for n in json.load(open(PD[-1]))["nodes"]} if PD else {}
RES = json.load(open(os.path.join(HERE, "..", "ch10-page", "resources_v1_0_0.json")))["links"]
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1 = ("Which operations on a path only compute a new path, which ask the file system a question, and which "
       "change files or folders, and what decides that?")
CQ2 = "Which printed outputs and concepts of the chapter differ in current Python or between operating systems, and on what source?"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in" % (group, w))
    h = round(lines_of(rr) * fs * 1.32 / 72.0 + 0.36, 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.083:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def prog(pname, x, y, w, fs=8, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'),
    as program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    maxlen = max(max(len(l) for l in shown), max((len(t) for t in out.split("\n")), default=0) + 8)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, w, fs))
    h = round((len(shown) + outlines) * fs * 1.32 / 72.0 + 0.40, 2)
    label = "program %s, lines %d to %d of %d - Python %s" % (pname, a, b, len(all_lines), PYV)
    if len(label) > (w - 0.1) / 0.083:
        label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: caption %r is too long for a %.1f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, h, fs=9, label="what the run printed"):
    """The transcript of a program beside its code: a panel holding only the lines the run printed."""
    out = PROGS[pname]["transcript"]
    fs = min(fs, round((w - 0.4) / ((max(len(t) for t in out.split("\n")) + 7) * 0.0088), 1))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
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
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


S = []


def content(title, sub, items, notes, take, lede=None):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 10: Paths and Files",
          "sub": "Naming a path, acting on a folder, and moving text and data through a file",
          "items": [{"t": "code", "x": 6.0, "y": 0.85, "w": 3.5, "h": 0.95, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Chapter 9 was about finding a pattern inside text you already had. This chapter is about where "
                   "that text lives: a path names a file without touching it, pathlib builds that name as an "
                   "object rather than a plain string, and once a path is in hand a program can create a folder, "
                   "search it, and read or write the file it names, whole or piece by piece. Every example on "
                   "these slides was run under Python 3.14.6 and the result printed beside it is the result "
                   "Python gave on this machine.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Six parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Six parts, from a path object to a saved shelf.",
          "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["5 branches", "%d concepts" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                     "Python %s" % PYV]}],
        "The first question is the chapter's own spine: a path method either only computes a new path object, "
        "such as with_suffix or the / operator, or it only asks the file system a question, such as exists(), or "
        "it actually changes a file or folder on disk, such as mkdir() or write_text(), and which of the three it "
        "is decides whether running it twice is safe. The second question is this chapter's own watch-out: the "
        "chapter was written and printed on Windows, so several of its own outputs, file lists, error messages, "
        "and even one printed quiz transcript, read differently once actually run on today's Python on a "
        "different operating system, and the research record keeps every such gap on the record rather than "
        "silently fixing it. The chips give the size of the chapter.",
        "A path's own method only computes, only asks, or actually changes a file.")

# ---- 4 path objects ---------------------------------------------------------------------------------------------
c, bot = con("pathobjects", 0.5, 1.5, 9.0, fs=11, label="Path() joins names into an object; / joins a path to a string or another path")
content("Path objects: building and joining a path", "Path() returns an object, not a string; the / operator joins it to more names",
        [c],
        "Path('spam', 'bacon', 'eggs') joins the names it is given with the separator of the operating system it "
        "runs on and returns a path object, not a string; str() is the separate step that turns that object back "
        "into text, which is why the chapter's own claim that Path() 'returns a string' is corrected the moment "
        "type() is actually called on it. The / operator does the identical join one step at a time and replaces "
        "the older os.path.join(), but it needs a path object on at least one side: 'spam' / 'bacon', two plain "
        "strings, raises TypeError, exactly as this console's own last row shows.",
        "Path() returns an object; / joins paths the way os.path.join() once did.")

# ---- 5 story: Pitrou 2012 ----------------------------------------------------------------------------------------
content("A 2012 proposal is why a path is an object", STORY["PitrouPathlib2012"]["when"],
        [card("Antoine Pitrou, PEP 428", "'The pathlib module - object-oriented filesystem paths', dated 30 July "
              "2012: a filesystem path should be its own object with its own methods, not a plain string passed "
              "to separate os.path functions.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "30 July 2012: PEP 428 is written, Antoine Pitrou",
             "Discussed through 2013 on python-dev",
             "Shipped in Python 3.4, March 2014",
             "Path() is an object because of this one proposal"]},
         factrow("PitrouPathlib2012")],
        story_notes("PitrouPathlib2012"),
        "Path() is an object because of Pitrou's 2012 proposal, PEP 428.")

# ---- 6 working locations ------------------------------------------------------------------------------------------
c, bot = con("workinglocations", 0.5, 1.5, 9.0, fs=12, label="Path.cwd() and Path.home() are both absolute; a relative path is read from cwd")
content("Working locations: the working directory and home", "A relative path is read from the working directory; Path.home() is always absolute",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "os.chdir() changes the working directory; pathlib has no method of its own for that one job. "
                  "A single dot names this folder and two dots its parent; a leading ./ is optional, which is why "
                  "Path('./spam.txt') and Path('spam.txt') compare equal."}],
        "Every running program has a current working directory, and a relative path such as Path('spam/bacon/"
        "eggs') is read starting from it; Path.cwd() and os.getcwd() both read that folder, and only os.chdir() "
        "changes it, which is why this console's own first row resets to a fixed folder before anything else "
        "runs. Path.home() returns the account's own home folder, always an absolute path wherever it is on "
        "disk, and Path.cwd().is_absolute() and Path.home().is_absolute() are both true for exactly that reason, "
        "while a plain relative path such as 'spam/bacon/eggs' is not.",
        "A relative path reads from cwd; Path.home() is always absolute.")

# ---- 7 path anatomy & derived paths --------------------------------------------------------------------------------
c, bot = con("pathanatomy", 0.5, 1.5, 9.0, fs=11, label="name, stem, suffix, drive and parent read a path apart; with_suffix and relative_to build a new one")
content("Path anatomy and derived paths", "A path breaks apart into name, stem, suffix and parent; with_suffix builds a new one",
        [c],
        "A path object breaks apart into named pieces with no disk touched at all: name is its very last part, "
        "stem is that name with its suffix removed, suffix is the extension itself, and drive names the Windows "
        "drive letter where one exists; parent is itself another path object, one level up, while parts is the "
        "same path read instead as an ordered tuple and parents an ordered sequence of every folder above it. "
        "with_suffix() and relative_to(), shown closing this console, build a brand-new path from an existing "
        "one's own pieces without ever reading or writing a file; the chapter itself, as printed, does not "
        "present either method.",
        "name, stem, suffix and parent read a path apart with no disk touched.")

# ---- 8 creating folders & finding files -----------------------------------------------------------------------------
c, bot = con("folders", 0.5, 1.5, 9.0, fs=9.5, label="mkdir(parents=True) creates every missing folder; glob('*.txt') lists a folder's own matching files")
content("Creating folders and finding files", "mkdir(parents=True) makes a whole chain of folders; a glob pattern lists matching files",
        [c],
        "Path.mkdir() makes exactly one folder and needs parents=True to also create every folder above it that "
        "is missing, exactly the way os.makedirs() always behaves on its own; both raise FileExistsError for a "
        "folder that is already there unless exist_ok=True is given. A glob pattern such as '*.txt' or the single-"
        "character '?' of 'project?.txt' searches one folder's own files, correctly leaving out a name such as "
        "project10.txt whose extra digit does not fit a single '?' at all; a ** segment or the dedicated rglob() "
        "method, not shown on this console, instead searches the whole tree of folders beneath one.",
        "mkdir(parents=True) builds a chain; a glob pattern lists matching names.")

# ---- 9 file information ---------------------------------------------------------------------------------------------
c, bot = con("fileinfo", 0.5, 1.5, 9.0, fs=11, label="exists(), is_file() and is_dir() never raise; stat() answers size and time together")
content("File information: exists, is_file, and stat", "exists(), is_file() and is_dir() ask without raising; stat() answers size and time",
        [c],
        "exists(), is_file() and is_dir() each answer a plain true or false about a path, every one of them False "
        "together for a path that is simply not there, and from Python 3.14 on none of the three raises an "
        "OSError even when the check itself is refused. stat() answers a richer question about a file that does "
        "exist: st_size is its size in bytes, and st_mtime, read here after being set by hand with os.utime(), is "
        "the time it was last changed, counted in seconds since 1 January 1970, which time.asctime(time.gmtime("
        "...)) turns back into a readable date exactly five hours away from the chapter's own local-time answer "
        "for the identical instant.",
        "exists/is_file/is_dir never raise; stat() answers size and time together.")

# ---- 10 whole file methods --------------------------------------------------------------------------------------
c, bot = con("wholefile", 0.5, 1.5, 9.0, fs=11, label="write_text/read_text move a whole string; write_bytes/read_bytes do the same for binary data")
content("Whole file methods: write_text and read_text", "One call each opens, acts, and closes; the character count returned is not a byte count.",
        [c],
        "write_text() creates or overwrites a file with a string in one call and returns the number of characters "
        "written, which is not always the number of bytes actually stored on disk: this console's own accented "
        "character, encoded as UTF-8, costs two bytes for the one character, so write_text() returns 4 while "
        "stat() then reports 5 bytes on disk for the same file. read_text() opens, reads and closes the file in "
        "one call as well, returning its whole content as one string; write_bytes() and read_bytes() do the "
        "identical one-call job for binary data such as b'\\x00\\x01\\xff', which has no text meaning at all and "
        "is never passed through an encoding.",
        "write_text() returns a character count, which is not a byte count.")

# ---- 11 opened files --------------------------------------------------------------------------------------------
c, bot = con("openedfiles", 0.5, 1.5, 9.0, fs=9, label="open() in mode r, w, a or x returns a file object read, written and closed by hand")
content("Opened files: modes, reading and closing", "open() returns a file object; read, readlines, write and close each act on it in turn",
        [c],
        "open() returns a file object in whichever mode it is given: 'r' reads and is the default, 'w' overwrites "
        "after emptying the file, 'a' appends to the end of it, and 'x' creates a brand-new file but raises "
        "FileExistsError the moment the name is already taken, exactly as this console's own last row shows. "
        "write() returns the number of characters written and, unlike print(), never adds its own newline; "
        "readlines() returns every remaining line as a list, and a file object remembers its own position between "
        "calls, so a second read right after readlines() returns only the empty string, until seek(0) moves that "
        "position back to the very start.",
        "open() in mode x fails the moment the file is already there.")

# ---- 12 story: Thompson and Pike, UTF-8 1992 -----------------------------------------------------------------------
content("UTF-8, designed on a 1992 diner placemat", STORY["ThompsonPikeUtf8"]["when"],
        [card("Ken Thompson and Rob Pike", "Rob Pike: UTF-8 was 'designed, in front of my eyes, on a placemat in a "
              "New Jersey diner' in September 1992, Thompson working out the bit-packing by hand; Plan 9 ran on it "
              "within the week.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "4 Sep 1992: first working Plan 9 code",
             "8 Sep 1992: proposal mailed to X/Open",
             "Bell Labs, Murray Hill, New Jersey",
             "'utf-8' in open() names this one dinner"]},
         factrow("ThompsonPikeUtf8")],
        story_notes("ThompsonPikeUtf8"),
        "'utf-8' in open() names a format from one 1992 dinner.")

# ---- 13 text encoding -----------------------------------------------------------------------------------------------
c, bot = con("textencoding", 0.5, 1.5, 9.0, fs=9, label="encoding chooses the byte-to-character map; errors chooses what happens when a byte cannot be mapped")
content("Text encoding: encoding, newline, and errors", "encoding converts bytes to characters; errors decides what happens to a byte it cannot map",
        [c],
        "The encoding argument names the map used to turn the bytes of a file into the characters of a string; "
        "'utf-8' is almost always the right choice, and reading the identical two-byte accented character under "
        "'ascii' instead raises UnicodeDecodeError, exactly as this console shows, because ascii has no mapping "
        "for a byte above 127 at all. The errors argument changes what happens next: 'replace', shown here, puts "
        "the placeholder character U+FFFD in an unreadable byte's place rather than stopping the program outright. "
        "The newline argument governs a separate translation, between the \\n Python always uses internally and "
        "whichever line ending the running operating system expects on disk.",
        "ascii cannot decode a byte above 127; errors='replace' papers over it.")

# ---- 14 automatic closing ---------------------------------------------------------------------------------------
c, bot = con("autoclose", 0.5, 1.5, 9.0, fs=13, label="a with statement closes the file on every way out of its block, even an exception")
content("Automatic closing: the with statement", "with closes a file however its block ends; a closed file raises ValueError if used again",
        [c,
         card("Why with, not close()", "A with statement's own __exit__ method is guaranteed to run once its "
              "__enter__ has returned, whether the block ends normally, returns early, or raises - a guarantee a "
              "bare close() call placed by hand can always be skipped by an exception in between.",
              0.5, bot + 0.12, 9.0, 4.95 - bot - 0.12, fs=12)],
        "A with statement creates a context manager and closes the file object the moment its own block is left, "
        "by reaching the block's end, by a return, or by an exception, which is why code written as with open(...)"
        " as file_obj: never needs close() called on it by hand at all. Once that block has ended, the file "
        "object's own closed attribute reads True, and a read or a write on it afterward raises exactly ValueError"
        ": I/O operation on closed file, the same error a file opened by hand and closed explicitly also raises "
        "once used again.",
        "A with block's file is closed on every way out, even an exception.")

# ---- 15 story: Thompson's dbm, 1979 -------------------------------------------------------------------------------
content("The file format behind a shelf is a 1979 idea", STORY["ThompsonDbm1979"]["when"],
        [card("Ken Thompson, dbm", "AT&T released dbm, written by Ken Thompson, in 1979: a key-value file with no "
              "query language and no server at all, exactly the shape shelve.open() still presents today.",
              0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1979: dbm, Ken Thompson, AT&T Bell Labs",
             "1991: Berkeley DB, a ndbm replacement",
             "Python's dbm picks a backend at run time",
             "A shelf's one-key-one-value shape is 1979's"]},
         factrow("ThompsonDbm1979")],
        story_notes("ThompsonDbm1979"),
        "A shelf's one-key-one-value file dates to Thompson's 1979 dbm.")

# ---- 16 shelves -------------------------------------------------------------------------------------------------
c, bot = con("shelves", 0.5, 1.5, 9.0, fs=10, label="shelve.open() behaves like a dictionary saved to disk; dbm.whichdb() names the backend it chose")
content("Shelves: a dictionary that outlives the program", "shelve.open() behaves like a dictionary; a changed mutable value can still be lost",
        [c],
        "shelve.open() opens a binary file on disk and hands back a shelf object that is read, written, counted "
        "and deleted from exactly like a dictionary, with keys() and values() both included, as long as every "
        "key is a string; close() must be called, or the shelf used in a with statement, before everything is "
        "reliably written out. A mutable value such as a list, read back out of a shelf and then changed in "
        "place with append(), is not noticed by the shelf at all unless it is assigned straight back to its key "
        "or the shelf is opened with writeback=True; dbm.whichdb(), shown closing this console, names dbm.sqlite3 "
        "as the backend chosen on this machine, first in line since Python 3.13.",
        "A shelf never notices a mutable value changed in place, unmarked.")

# ---- 17 story: Crockford, JSON 2001 --------------------------------------------------------------------------------
content("A 2001 write-up is shelve's plain alternative", STORY["CrockfordJson2001"]["when"],
        [card("Crockford and Morningstar", "At State Software, the two wrote up a minimal, quoted-key "
              "format in 2001 so a browser and a server could exchange data without a page reload; Crockford "
              "opened json.org on 12 November 2002.", 0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "2001: the format is written up, State Software",
             "12 Nov 2002: json.org opens",
             "Designed small enough for a business card",
             "json.dump/load replace shelve's own pickle"]},
         factrow("CrockfordJson2001")],
        story_notes("CrockfordJson2001"),
        "json, shelve's plain alternative, was written up in 2001.")

# ---- 18 json saving ---------------------------------------------------------------------------------------------
c, bot = con("jsonsaving", 0.5, 1.5, 9.0, fs=15, label="json.dumps/loads round-trip plain data as text; a tuple comes back a list, an int key a string")
content("Plain alternative: saving data as json", "json writes plain data as readable text any program can read; a tuple comes back as a list",
        [c,
         card("What json cannot keep", "A tuple written with json.dumps() always comes back as a list, and a "
              "non-string dictionary key such as the integer 5 always comes back as the string '5'; shelve, by "
              "contrast, keeps both exactly, at the cost of being readable only by Python's own pickle.",
              0.5, bot + 0.12, 9.0, 4.95 - bot - 0.12, fs=12.5)],
        "json.dump() and json.load() move plain data, strings, numbers, lists, dictionaries, true, false and "
        "null, between a Python program and a text file that any other program or language can also read, unlike "
        "a shelf's own Python-only pickle format. json.dumps() of a dictionary holding a tuple and an integer key "
        "shows exactly where that plain-text format falls short of Python's own richer types: the tuple is "
        "printed, and read back, as a plain list, and the integer key 5 is printed, and read back, as the string "
        "'5', neither loss something shelve's own binary format would ever make.",
        "json keeps every value readable, but a tuple becomes a list.")

# ---- 19 Project 4: the quiz generator --------------------------------------------------------------------------------
p1, bot = prog("capitalsQuiz_v1_0_0.py", 0.5, 1.5, 9.0, fs=7, lines=(48, 56), show_out=False)
p2 = transcript("capitalsQuiz_v1_0_0.py", 0.5, bot + 0.2, 9.0, 1.75,
                fs=7, label="prints: the start of quiz 1 and its answer key, one unbroken line, letters only")
content("Project 4: the state capitals quiz generator", "A dictionary of 50 capitals, shuffled per quiz, written to a quiz file and an answer key",
        [p1, p2],
        "Project 4 keeps the 50 states and their capitals in one dictionary, shuffles the order of the states for "
        "each quiz, picks three wrong capitals at random for every question with random.sample(), shuffles those "
        "three together with the one right answer, and writes both a quiz file and an answer key file for each "
        "pass of its own loop, two files per quiz, seventy files in all across the chapter's own thirty-five. Run "
        "exactly as the chapter lists the code, with random.seed(10) added only so this result can be checked "
        "again, it reproduces the chapter's own research record in full: the header prints with no space at all, "
        "'(Form1)', and the whole answer key is written as one unbroken line with no newline between its own "
        "answers, a real gap between the chapter's prose and the code it actually lists, not a mistake introduced "
        "here.",
        "The chapter's own listed code writes '(Form1)' and one joined key line.")

# ---- 20 practice: Mad Libs -------------------------------------------------------------------------------------
p1, bot = prog("madLibs_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(7, 15), show_out=False)
p2 = transcript("madLibs_v1_0_0.py", 0.5, bot + 0.2, 9.0, 1.5,
                fs=8, label="typed: silly, chandelier, screamed, pickup truck - one answer per blank, in order")
content("Practice: Mad Libs with a regex replacement", "re.sub() with a function asks for a new word at every ADJECTIVE, NOUN, ADVERB or VERB",
        [p1, p2],
        "Practice program 1 reads a short text file holding the placeholders ADJECTIVE, NOUN, ADVERB and VERB, "
        "and re.sub() with a function in place of a replacement string calls that function once for every match, "
        "in the order the placeholders appear, asking the user for one new word each time; the four answers typed "
        "here, silly, chandelier, screamed and pickup truck, fill the chapter's own four blanks in exactly that "
        "order. The finished string is printed and then saved to a brand-new file with write_text(), leaving the "
        "original source file untouched, and read back afterward to confirm the two copies are equal character "
        "for character.",
        "re.sub() with a function asks for one new word at each match, in order.")

# ---- 21 practice: regex search, and questions -----------------------------------------------------------------------
p1 = {**prog("regexSearchFiles_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(7, 26), show_out=True)[0]}
p1["h"] = 3.65
content("Practice: searching files, and chapter questions", "glob('*.txt') lists the files; enumerate(f, start=1) numbers every line a pattern matches",
        [p1],
        "Practice program 2 opens every .txt file a folder's own glob('*.txt') lists, and prints each line in any "
        "of them that matches a regular expression typed in by the user, with enumerate(f, start=1) numbering "
        "every line as it is read; the one .csv file in this console's own folder is correctly left out of every "
        "search. The chapter's own eleven practice questions close the chapter the same way this deck's own "
        "summary closes it, asking a reader to say in their own words what a relative path, an absolute path, "
        "the open() modes, and a shelf's own dictionary-like behaviour each actually are, every one of them "
        "answered exactly once already on an earlier slide.",
        "glob('*.txt') lists the files a user-typed pattern then searches.")

# ---- 22 summary ------------------------------------------------------------------------------------------------------
content("The chapter in six lines", "One line for each part of the route",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 11.5, "items": [
            "Path() returns an object, not a string; / joins it to more names the way os.path.join() once did.",
            "A relative path reads from the working directory; name, stem, suffix and parent read a path apart.",
            "mkdir(parents=True) builds a chain of folders; a glob pattern lists the files that match it.",
            "write_text/read_text move a whole file in one call; open() in mode r, w, a or x returns a file object.",
            "The encoding argument converts bytes to characters; a with block closes its file on every way out.",
            "A shelf behaves like a dictionary saved to disk; json keeps the same data readable by any program."]}],
        "These six lines answer the route one part at a time. The first two cover a path as an object and the "
        "pieces it breaks into, the third covers a folder, the fourth and fifth cover a file opened by hand and "
        "the arguments that decide how its bytes become characters, and the sixth covers a program's own "
        "variables saved for a later run. If a line feels unproven, the part of the route that carries it has "
        "the slides with the executed examples.",
        "If a line feels unproven, its slides hold the example.")

# ---- 23 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(":")[0] if r["kind"] != "documentation" or "textbook" not in r["title"].lower() else "The textbook, chapter 10 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


_docs = rows(("documentation",))
_peps = rows(("pep",))
_byname = {d[0]: d for d in _docs}


def pick(*keys):
    out = []
    for k in keys:
        out.append(next(d for d in _docs if k.lower() in d[0].lower()))
    return out


_read = pick("boring stuff", "pathlib", "shelve")
_ref = pick("open", "os", "json")
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read},
            {"head": "Reference", "rows": _ref},
            {"head": "PEPs and history", "rows": _peps + [
                ["Rob Pike's UTF-8 history", STORY["ThompsonPikeUtf8"]["link"]]]}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read "
        "online and has Project 4 and both practice programs in full, the reference links are the official "
        "documentation behind every quirk this deck flagged, and the PEPs and history links are the primary "
        "sources behind this chapter's own four stories and the two language changes, UTF-8 mode and the pathlib "
        "protocol, that most directly touch this chapter's own code.",
        "History, documentation and PEPs, opened the day this deck was built.")

# ---- 24 closing -------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "Path() returns an object; a method either computes a path, asks a question, or changes the disk.",
            "write_text/read_text and open() in mode r, w, a or x both read and write a file, whole or by hand.",
            "The encoding argument converts bytes to characters; a with block closes its file no matter how it ends.",
            "A shelf behaves like a dictionary saved to disk; json keeps the same plain data readable by any program."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d console rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the "
        "examples yourself, you have the chapter. The next chapter moves on from a program's own files to the web "
        "pages it can read.",
        "Questions are welcome; bring one path operation you could not predict.")

# ---- agenda -----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Filepaths: path objects and working locations", "Path objects: building and joining a path", "Path anatomy and derived paths"),
          ("Folders and file information", "Creating folders and finding files", "File information: exists, is_file, and stat"),
          ("Text files: whole methods, opened files, encoding", "Whole file methods: write_text and read_text", "Automatic closing: the with statement"),
          ("Saved data: shelves and the plain alternative", "The file format behind a shelf is a 1979 idea", "Plain alternative: saving data as json"),
          ("Chapter programs: the quiz, Mad Libs, and search", "Project 4: the state capitals quiz generator", "Practice: searching files, and chapter questions"),
          ("Summary and resources", "The chapter in six lines", "Where to go from here")]
_rows = []
for name, a, b in _parts:
    _rows.append("%s (slides %d-%d)" % (name, _t[a], _t[b]))
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(5)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": str(len(ST.STORIES)), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["notes"] = ("The route has six parts. It starts with filepaths, a path as an object and the pieces it "
                 "breaks into, moves to folders and file information, then to text files, opened by hand and "
                 "converted between bytes and characters, then to saved data, a shelf and its plain alternative, "
                 "then to the chapter's own programs, the quiz generator and the two practice programs, and ends "
                 "with the summary and resources. The ranges name the exact slides, so you can return to the part "
                 "you need, and four of the slides are true stories that explain where a piece of this chapter's "
                 "own vocabulary came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 10: Reading and Writing Files", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
