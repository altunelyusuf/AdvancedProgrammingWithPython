#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 11 (Organizing Files) on the CME classroom standard.

Same regime as chapter 10: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
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


ST = load("stories4111", os.path.join(HERE, "..", "sen0414_ch11_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
PD = sorted(__import__("glob").glob(os.path.join(HERE, "..", "ch11-page", "page_data_v*.json")),
            key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = {n["id"]: n for n in json.load(open(PD[-1]))["nodes"]} if PD else {}
RES = json.load(open(os.path.join(HERE, "..", "ch11-page", "resources_v1_0_0.json")))["links"]
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1 = ("Which file operations of the chapter change the disk for good, which can be undone, and how can a "
       "program show what it will do before it does it?")
CQ2 = "Which printed outputs, statements and programs of the chapter differ in current Python, and on what source?"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in" % (group, w))
    L = lines_of(rr)
    h = round(L * fs * 1.32 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
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
    L = len(shown) + outlines
    h = round(L * fs * 1.32 / 72.0 + 0.40 + 0.02 * max(0, L - 1), 2)
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
S.append({"kind": "title", "title": "Chapter 11: Organizing Files",
          "sub": "Copying, moving, deleting, walking and archiving files with shutil, os and zipfile",
          "items": [{"t": "code", "x": 6.0, "y": 0.85, "w": 3.5, "h": 0.95, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Chapter 10 was about one file at a time, read or written through a path. This chapter moves "
                   "up to whole files and folders: shutil copies and moves them, os and shutil delete them, "
                   "os.walk and pathlib visit every folder in a tree, and zipfile packs a tree into one archive "
                   "and takes it back out again. Every example on these slides was run under Python 3.14.6 and "
                   "the result printed beside it is the result Python gave on this machine.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Six parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Six parts, from copying a file to a numbered backup archive.",
          "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["5 branches", "%d concepts" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                     "Python %s" % PYV]}],
        "The first question is this chapter's own spine: shutil.copy and shutil.copytree keep the source and "
        "leave it untouched, shutil.move removes it, and os.unlink, os.rmdir and shutil.rmtree remove something "
        "for good with no copy left anywhere, so a dry run, a print in the dangerous call's place, is the "
        "chapter's own answer for seeing the damage before it happens. The second question is this chapter's own "
        "watch-out: the chapter's own prose and its own listed code disagree in at least two places, a move onto "
        "an existing name and the size the chapter's own ZIP example claims to compress to, and this deck's own "
        "research record keeps every such gap on the record rather than silently fixing it. The chips give the "
        "size of the chapter.",
        "Copy and copytree keep the source; delete, unlink and rmtree do not.")

# ---- 4 copying --------------------------------------------------------------------------------------------------
c, bot = con("copying", 0.5, 1.5, 9.0, fs=9.5, label="shutil.copy keeps the source; copytree needs a new destination unless dirs_exist_ok=True")
content("Copying: shutil.copy and shutil.copytree", "A copy keeps the source in place; copy2 also keeps its modification time",
        [c],
        "shutil.copy(source, destination) copies one file to a folder, which keeps the name, or to a file name, "
        "which becomes the copy's own name, and shutil.copytree copies a whole folder with everything in it to a "
        "destination that must not already exist, unless dirs_exist_ok=True lets it continue into one that is "
        "already there, overwriting only the files of the same name. Neither function is in the chapter's own "
        "prose returning anything useful, but both return the path they wrote to, and shutil.copy2, which "
        "copytree itself uses internally for every file, keeps metadata such as the modification time that a "
        "plain shutil.copy does not, as this console's own os.utime() row shows directly.",
        "shutil.copy and copytree keep the source; copy2 also keeps the metadata.")

# ---- 5 moving ---------------------------------------------------------------------------------------------------
c, bot = con("moving", 0.5, 1.5, 9.0, fs=8.5, label="shutil.move relocates or renames; a name already in the destination raises shutil.Error, not an overwrite")
content("Moving: shutil.move and the pathlib methods", "shutil.move both relocates and renames; Python 3.14 added Path.copy and move",
        [c],
        "shutil.move(source, destination) moves a file or folder to a destination; when that destination is an "
        "existing folder the source goes inside it under its own name, and when it is not, the call renames in "
        "place, so one function covers both jobs depending only on what the destination turns out to be. The "
        "chapter's own prose says a same-named file in the destination would be overwritten; run under 3.14.6 "
        "the call instead raised shutil.Error and moved nothing at all, leaving the old file and the source both "
        "exactly where they were, which is what the documentation itself promises rather than what the chapter's "
        "own prose claims. Since Python 3.14 a Path object can copy and move itself directly, Path.copy and "
        "Path.move, without importing shutil at all, shown closing this console.",
        "A same name in the destination refuses the move; it does not overwrite it.")

# ---- 6 deleting -------------------------------------------------------------------------------------------------
c, bot = con("deleting", 0.5, 1.5, 9.0, fs=9, label="os.unlink deletes a file, os.rmdir an empty folder, shutil.rmtree a whole tree, all permanently")
content("Deleting: unlink, rmdir, and rmtree", "Three functions delete for good; onexc, since 3.12, lets rmtree skip past one failure",
        [c],
        "os.unlink(path) deletes one file permanently, os.rmdir(path) deletes one folder and only if it is "
        "empty, raising OSError otherwise, and shutil.rmtree(path) deletes a whole folder tree with everything "
        "in it in a single call; all three raise FileNotFoundError for a path that is not there at all, except "
        "rmtree with ignore_errors=True, which raises nothing. Since Python 3.12 the onexc parameter names a "
        "function that receives the failing function, the path and the exception itself, so a tree with one "
        "missing folder can be walked past rather than stopping rmtree at its very first failure, which this "
        "console's own closing rows show directly, a missing folder's own name paired with FileNotFoundError.",
        "unlink, rmdir and rmtree delete for good; none of the three can be undone.")

# ---- 7 story: Kare, the 1983 trash icon --------------------------------------------------------------------------
content("The recycle bin's own icon is a 1983 drawing", STORY["KareTrashIcon1983"]["when"],
        [card("Susan Kare, Apple", "Kare joined Apple in 1983 with no graphics training at all and drew the "
              "trash can on a 32-by-32 pixel grid in Andy Hertzfeld's own icon editor; it shipped on the "
              "Macintosh desktop in 1984.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1983: Kare joins Apple, no graphics training",
             "32x32 pixel grid, Andy Hertzfeld's icon editor",
             "1984: the trash can ships on the Macintosh",
             "send2trash still moves a file to this one bin"]},
         factrow("KareTrashIcon1983")],
        story_notes("KareTrashIcon1983"),
        "send2trash's bin is Kare's own 1983 Macintosh trash icon.")

# ---- 8 safer deletion ---------------------------------------------------------------------------------------------
c, bot = con("saferdeletion", 0.5, 1.5, 9.0, fs=15, label="a dry run replaces the dangerous call with a print; a typo in a pattern then matches nothing at all")
content("Safer deletion: the dry run and the recycle bin", "A print in the delete's place shows the damage first; send2trash moves files instead",
        [c,
         card("Why this matters", "The chapter's own typo, glob('*.rxt') for '*.txt', would quietly delete "
              "nothing - the dry run matches zero files for the typo, both for the fix. send2trash is not "
              "installed here.", 0.5, bot + 0.12, 9.0, 4.95 - bot - 0.12, fs=12)],
        "A dry run replaces a dangerous call, a delete, a copy, a rename or a move, with a print that shows "
        "exactly what the real call would touch, and the chapter's own worked example is a typo: glob('*.rxt') "
        "in place of '*.txt' would delete nothing visible until it was too late, where the dry run's own print "
        "matches zero files against the broken pattern and both files against the corrected one. The third-party "
        "send2trash module moves a file or folder to the recycle bin or trash instead of deleting it outright, so "
        "a mistake stays recoverable, though it frees no disk space and cannot take anything back out of the bin "
        "on its own; it is not installed on this machine, so nothing about it runs in this deck.",
        "A dry run prints what a delete would do, before it actually runs.")

# ---- 9 listing --------------------------------------------------------------------------------------------------
c, bot = con("listing", 0.5, 1.5, 9.0, fs=11, label="os.listdir and Path.iterdir list one folder; glob and rglob match names with a wildcard pattern")
content("Listing: names, path objects, and glob patterns", "os.listdir and Path.iterdir list one folder; glob and rglob match a wildcard pattern",
        [c],
        "os.listdir(path) returns the names inside one folder as a list of strings, and Path.iterdir() gives the "
        "identical entries back as path objects instead, each one ready for is_dir() or is_file() without a "
        "second call; neither one looks inside a subfolder at all. A glob pattern such as '*.txt', the exact "
        "pattern the chapter's own deletion example matches against, searches one folder with Path.glob, and "
        "Path.rglob searches every subfolder beneath it as well, so against a.txt, b.pdf and a nested c.txt, glob "
        "found only a.txt and rglob found both a.txt and c.txt.",
        "listdir and iterdir list one folder; glob and rglob match a wildcard.")

# ---- 10 story: Daley and Neumann, the 1965 Multics tree ------------------------------------------------------------
content("The folder tree os.walk visits is a 1965 design", STORY["DaleyNeumannMultics1965"]["when"],
        [card("R.C. Daley and P.G. Neumann", "The pair presented Multics's own tree-structured file system at "
              "the 1965 Fall Joint Computer Conference; Ken Thompson and Dennis Ritchie, who had worked on "
              "Multics, carried the same tree into Unix soon after.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1965: Fall Joint Computer Conference paper",
             "R.C. Daley, MIT Project MAC; P.G. Neumann, Bell Labs",
             "Thompson and Ritchie carry the tree into Unix",
             "os.walk still descends this same 1965 shape"]},
         factrow("DaleyNeumannMultics1965")],
        story_notes("DaleyNeumannMultics1965"),
        "os.walk descends the folder tree Daley and Neumann designed in 1965.")

# ---- 11 walking -------------------------------------------------------------------------------------------------
c, bot = con("walking", 0.5, 1.5, 9.0, fs=10, label="os.walk gives a folder before its subfolders by default; topdown=False reverses that order")
content("Walking: os.walk and Path.walk", "Each pass of os.walk hands back a folder, its subfolders and files; topdown sets the order",
        [c],
        "for folder_name, subfolders, filenames in os.walk(top) visits a folder and every folder beneath it, "
        "handing back on each pass the current folder's name as a string, its own subfolder names and its own "
        "file names; by default a folder comes before its subfolders, and topdown=False reverses that into the "
        "bottom-up order needed to empty a tree with rmdir, exactly as the standard library's own rmtree example "
        "does. Path.walk, added in Python 3.12, is the identical loop for path objects, handing back a Path "
        "rather than a plain string for the current folder, and a program walking top-down can prune a whole "
        "folder out of the rest of the walk simply by removing its name from the subfolder list in place.",
        "A folder comes before its subfolders by default; topdown=False reverses it.")

# ---- 12 story: Phil Katz, ZIP 1989 ---------------------------------------------------------------------------------
content("The ZIP format was given away free on 14 Feb 1989", STORY["PhilKatzZip1989"]["when"],
        [card("Phil Katz, PKWARE", "After a lawsuit over his own earlier archiver, Katz and Gary Conway designed "
              "a new format and placed it in the public domain on 14 February 1989, free for any program to read "
              "or write.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "14 Feb 1989: public-domain press release",
             "Phil Katz and Gary Conway, PKWARE",
             "APPNOTE.TXT ships that year in PKZIP 0.9",
             "zipfile reads and writes this one format"]},
         factrow("PhilKatzZip1989")],
        story_notes("PhilKatzZip1989"),
        "zipfile reads the format PKWARE gave away free on 14 Feb 1989.")

# ---- 13 writing zip ---------------------------------------------------------------------------------------------
c, bot = con("zipwriting", 0.5, 1.5, 9.0, fs=9.5, label="mode 'w' erases and starts fresh, mode 'a' keeps and adds, mode 'x' refuses an existing file")
content("Writing zip archives: modes and compression", "ZipFile opens in mode w, a or x; write() compresses only with ZIP_DEFLATED",
        [c],
        "zipfile.ZipFile(name, 'w') creates a new archive, erasing one that already exists, and write() adds a "
        "file from disk under its own path, compressing it only when compress_type=zipfile.ZIP_DEFLATED is "
        "actually passed; without it, a file is stored at its own regular size, which is exactly the gap "
        "between the chapter's own two ZIP examples, one compressed and one not. Mode 'a' instead keeps what is "
        "already in the archive and adds to it, and mode 'x', not in the chapter's own prose at all, refuses to "
        "touch a file that already exists, raising FileExistsError the moment its name is already taken, "
        "exactly as this console's own closing row shows.",
        "write() only compresses when ZIP_DEFLATED is actually passed to it.")

# ---- 14 story: Gailly and Adler, zlib 1995 --------------------------------------------------------------------------
content("Compression under ZIP_DEFLATED began free in 1995", STORY["GaillyAdlerZlib1995"]["when"],
        [card("Gailly and Adler, zlib", "Jean-Loup Gailly and Mark Adler released zlib 0.9 on 1 May 1995, a free "
              "implementation of DEFLATE built first for the libpng image library, owing nothing to Phil Katz's "
              "own patented code.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1 May 1995: zlib 0.9 released, free of charge",
             "Jean-Loup Gailly (compress), Mark Adler (decompress)",
             "Built first for Thomas Boutell's libpng",
             "ZIP_DEFLATED calls this same library"]},
         factrow("GaillyAdlerZlib1995")],
        story_notes("GaillyAdlerZlib1995"),
        "ZIP_DEFLATED runs zlib, free since Gailly and Adler's 1995 release.")

# ---- 15 reading zip ---------------------------------------------------------------------------------------------
c, bot = con("zipreading", 0.5, 1.5, 9.0, fs=13, label="namelist lists every member's own name; getinfo answers one member's own original and compressed size")
content("Reading zip archives: namelist and getinfo", "namelist lists every member; getinfo's two sizes say how well one member compressed",
        [c],
        "zipfile.ZipFile(name) opens an archive for reading, and namelist() returns every member's own name as a "
        "list of strings, a folder entry appearing with a closing slash; getinfo('file1.txt') then returns a "
        "ZipInfo whose file_size and compress_size hold that one member's own original and compressed size. The "
        "chapter divides those two numbers and prints 'Compressed file is 515.46x smaller!', a line that "
        "reproduces exactly under 3.14.6 for fifty thousand bytes stored in ninety-seven, while the chapter's own "
        "separate prose puts the compressed size at about 213 bytes, a figure that neither compresslevel 9 nor "
        "the default level 6 actually gives.",
        "getinfo's two sizes divide into the ratio the chapter's own line prints.")

# ---- 16 extracting zip --------------------------------------------------------------------------------------------
c, bot = con("zipextracting", 0.5, 1.5, 9.0, fs=10, label="extractall takes every member out; extract takes one, by a name that must be in namelist already")
content("Extracting zip archives and staying safe", "extractall writes every member into a folder; the module keeps a hostile name contained",
        [c],
        "extractall() writes every member of an archive into the current folder, or into a named one created "
        "when missing, overwriting files of the same name without asking, and extract('file1.txt', folder) does "
        "the identical job for one chosen member, raising KeyError the moment that name is not actually one "
        "namelist() returns. The chapter never warns about an untrusted archive at all, but the module itself "
        "already strips a member name such as '../../evil.txt' or a leading slash down to something that stays "
        "inside the target folder, which is why the documentation's own advice to inspect an archive first is "
        "still worth repeating rather than relied on alone.",
        "extractall overwrites without asking; a hostile member name stays contained.")

# ---- 17 archive helpers -------------------------------------------------------------------------------------------
c, bot = con("archivehelpers", 0.5, 1.5, 9.0, fs=10, label="shutil.make_archive builds a whole archive in one call; shutil.unpack_archive extracts it back")
content("Archive helpers: make_archive and unpack_archive", "shutil builds and extracts a whole archive in one call, by its own extension",
        [c],
        "shutil.make_archive(base_name, 'zip', root_dir, base_dir) builds a ZIP archive of a whole folder in a "
        "single call and returns the archive's own name, deflating every file inside it by default, which is "
        "more compression than the chapter's own hand-written write() calls ever ask for on their own. "
        "shutil.unpack_archive(filename, extract_dir) is the matching single call the other way, choosing the "
        "archive's own format from its file name's extension and using the zipfile module underneath for a ZIP "
        "file exactly as extractall does, neither helper appearing in the chapter's own prose at all.",
        "make_archive and unpack_archive replace write() and extractall at once.")

# ---- 18 backup project ------------------------------------------------------------------------------------------
p1, bot = prog("backupProject_v1_0_0.py", 0.5, 1.5, 9.0, fs=7, lines=(21, 24), show_out=False)
p2 = transcript("backupProject_v1_0_0.py", 0.5, bot + 0.2, 9.0, 2.35,
                fs=7, label="prints: creating, walking and finishing one archive, then naming the very next one")
content("Project 5: backing a folder up into a ZIP", "The program names the next unused archive, walks the folder, and writes every file found",
        [p1, p2],
        "Project 5 first works out the archive's own name, the folder's last path part, an underscore and a "
        "number that grows until no file of that name exists yet, then opens a ZipFile in write mode and, inside "
        "os.walk, writes every file it finds with backup_zip.write(folder_name / filename). Run exactly as the "
        "chapter lists the code, it reproduces the chapter's own research record in full: the archive is opened "
        "with no compression type at all, so it is never actually compressed, and a second run against the same "
        "folder correctly names the next number in turn, spam_2.zip rather than overwriting spam_1.zip, exactly "
        "as next zip name's own worked example predicts.",
        "The archive is stored, not compressed, and each run gets the next number.")

# ---- 19 practice: selective copy ---------------------------------------------------------------------------------
p1, bot = prog("selectiveCopy_v1_0_0.py", 0.5, 1.5, 9.0, fs=9, lines=(7, 14), show_out=True)
content("Practice: copying files of one chosen extension", "os.walk finds every file; lower-casing the name matches an extension regardless of case",
        [p1],
        "The first practice program walks a tree with os.walk and copies every file whose name ends in a chosen "
        "extension into a new folder with shutil.copy, and comparing the lower-cased name rather than the plain "
        "extension is exactly what lets two.PDF, written with capital letters, still match '.pdf' alongside "
        "one.pdf and four.pdf. three.txt, the one file of a different extension inside the same tree, is "
        "correctly left behind in the source tree rather than copied at all, confirming the extension test does "
        "its one job and nothing more.",
        "Lower-casing the name before the test matches two.PDF as well as one.pdf.")

# ---- 20 practice: date renaming, and chapter questions ------------------------------------------------------------
p1 = {**prog("dateRenaming_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(6, 20), show_out=True)[0]}
p1["h"] = 3.65
content("Practice: swapping a date, and chapter questions", "re.sub with reordered groups swaps MM-DD-YYYY to DD-MM-YYYY; move renames it",
        [p1],
        "The fourth practice program matches the pattern (\\d\\d)-(\\d\\d)-(\\d\\d\\d\\d) against a file's own "
        "name and calls re.sub with its own three groups reordered 2, 1, 3, turning spam12-31-1900.txt into "
        "spam31-12-1900.txt and report01-02-2020.txt into report02-01-2020.txt, while shutil.move actually "
        "carries out each rename; notes.txt, carrying no date at all, is correctly left alone by the pattern. "
        "The chapter's own eleven practice questions close the chapter the same way this deck's own summary "
        "closes it, asking a reader to say in their own words what shutil.copy, shutil.move, a dry run and the "
        "ZipFile method equivalent to open() each actually are, every one of them answered exactly once already "
        "on an earlier slide.",
        "re.sub with reordered groups swaps the date; shutil.move renames it.")

# ---- 21 summary -----------------------------------------------------------------------------------------------------
content("The chapter in six lines", "One line for each part of the route",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 11.5, "items": [
            "shutil.copy and copytree keep the source; shutil.move and the Path methods of 3.14 do not.",
            "os.unlink, os.rmdir and shutil.rmtree delete for good; a dry run previews any of them first.",
            "os.listdir, Path.iterdir and a glob pattern list a folder; os.walk and Path.walk visit a whole tree.",
            "zipfile.ZipFile writes, in mode w, a or x, and reads namelist and getinfo back from what it wrote.",
            "extractall and extract take files back out; the module itself keeps a hostile name inside the folder.",
            "The backup project names the next archive, walks the folder, and stores every file it finds."]}],
        "These six lines answer the route one part at a time. The first two cover copying, moving and deleting a "
        "file or folder, the third covers reaching every file of a tree, the fourth and fifth cover writing, "
        "reading and extracting a ZIP archive, and the sixth covers the chapter's own backup project, which "
        "walks a tree exactly as the third line's own os.walk does. If a line feels unproven, the part of the "
        "route that carries it has the slides with the executed examples.",
        "If a line feels unproven, its slides hold the example.")

# ---- 22 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(":")[0] if r["kind"] != "documentation" or "textbook" not in r["title"].lower() else "The textbook, chapter 11 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


_docs = rows(("documentation",))
_peps = rows(("pep",))


def pick(*keys):
    out = []
    for k in keys:
        out.append(next(d for d in _docs if k.lower() in d[0].lower()))
    return out


_read = pick("boring stuff", "shutil", "zipfile")
_ref = pick("os —", "pathlib", "zlib")
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read},
            {"head": "Reference", "rows": _ref},
            {"head": "History", "rows": [
                ["ZIP (file format), Wikipedia", STORY["PhilKatzZip1989"]["link"]],
                ["zlib, Wikipedia", STORY["GaillyAdlerZlib1995"]["link"]],
                ["Kare's trash icon", STORY["KareTrashIcon1983"]["link"]],
                ["Multics History", STORY["DaleyNeumannMultics1965"]["link"]]]}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read "
        "online and has Project 5 and all four practice programs in full, the reference links are the official "
        "documentation behind every quirk this deck flagged, and the history links are the primary sources "
        "behind this chapter's own four stories, the format, the compression library, the recycle bin's icon and "
        "the folder tree itself.",
        "History, documentation and the textbook, opened the day this deck was built.")

# ---- 23 closing -------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "shutil.copy and copytree keep the source; shutil.move and unlink, rmdir, rmtree do not.",
            "A dry run, a print in a dangerous call's place, shows the damage before it actually happens.",
            "os.walk and Path.walk visit a whole tree; glob and rglob match a wildcard against one or all of it.",
            "ZipFile writes and reads an archive; make_archive and unpack_archive do the same job in one call."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the "
        "examples yourself, you have the chapter. The next chapter moves on from a program's own files to the web "
        "pages it can read.",
        "Questions are welcome; bring one archive quirk you could not predict.")

# ---- agenda -----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Copying and moving: shutil relocates and renames", "Copying: shutil.copy and shutil.copytree", "Moving: shutil.move and the pathlib methods"),
          ("Deleting: permanent functions, and staying safe", "Deleting: unlink, rmdir, and rmtree", "Safer deletion: the dry run and the recycle bin"),
          ("Folder trees: listing one folder, walking a whole tree", "Listing: names, path objects, and glob patterns", "Walking: os.walk and Path.walk"),
          ("Zip archives: writing, reading, extracting, and shutil's own helpers", "The ZIP format was given away free on 14 Feb 1989", "Archive helpers: make_archive and unpack_archive"),
          ("Backup project and the chapter's own practice programs", "Project 5: backing a folder up into a ZIP", "Practice: swapping a date, and chapter questions"),
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
S[1]["notes"] = ("The route has six parts. It starts with copying and moving, which both keep or lose the "
                 "source depending on the function, moves to deleting, where a dry run and the recycle bin are "
                 "the chapter's own two safeguards, then to folder trees, listing one folder and walking a "
                 "whole one, then to zip archives, writing, reading, extracting and shutil's own one-call "
                 "helpers, then to the chapter's own backup project and its practice programs, and ends with "
                 "the summary and resources. The ranges name the exact slides, so you can return to the part you "
                 "need, and four of the slides are true stories that explain where a piece of this chapter's own "
                 "vocabulary came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 11: Organizing Files", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
