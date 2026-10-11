#!/usr/bin/env python3
"""SEN0414, chapter 11 (Organizing Files, Automate the Boring Stuff with Python, 3rd edition) - the
narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a
use-case diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and
its parts a mind map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the
narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry
names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was
read from (also_from names further concepts whose explanations the content draws on), one sentence saying why the
pattern fits, and the diagram's content in the element names the renderer of that type expects. Every element label
is made of words that occur in the explanations of the accompanying concepts or their section; run_checks() measures
that (the grounding ratio) besides the structural rules. This module follows the layout of
sen0414_ch10_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of
another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ChoosingAFileOperation",
        "pattern": "Workflow",
        "title": "What kind of thing an operation on a file does",
        "concepts": ["CopyFile", "MoveFileOrFolder", "DeleteFile", "DryRun"],
        "also_from": ["Copying", "Moving", "PermanentDeletion", "SaferDeletion", "CopyingAndMoving", "Deleting"],
        "read_from": "chapter 11, the copying, moving and deleting sections: shutil.copy copies a file and keeps "
                     "the source, shutil.move moves a file and removes the source, os.unlink deletes a file for "
                     "good, and a dry run replaces any of these with a print before the real call runs",
        "why": "the explanations describe what a programmer decides, in order, before one call touches a file - "
               "should the call be tried safely first with a print, does the file need to be gone for good, or "
               "does the source stay or go - with a different answer reached on each branch: a workflow with "
               "choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "Copying, moving and deleting a file"},
                {"id": "dry", "label": "Dry run: print before delete, copy or move", "kind": "decision"},
                {"id": "doprint", "label": "The print runs instead of the delete, copy or move"},
                {"id": "perm", "label": "Permanent deletion removes the file for good", "kind": "decision"},
                {"id": "delete", "label": "os.unlink deletes the file for good"},
                {"id": "copymove", "label": "Copy the file, or move it", "kind": "decision"},
                {"id": "copynode", "label": "shutil.copy keeps the source; the destination is the copy"},
                {"id": "movenode", "label": "shutil.move moves the file and deletes the source"},
            ],
            "flows": [["start", "need"], ["need", "dry"], ["dry", "doprint", "yes"], ["dry", "perm", "no"],
                      ["perm", "delete", "yes"], ["perm", "copymove", "no"], ["copymove", "copynode", "copy"],
                      ["copymove", "movenode", "move"], ["doprint", "end"], ["delete", "end"], ["copynode", "end"],
                      ["movenode", "end"]],
        },
    },
    {
        "id": "ChoosingAZipFileMode",
        "pattern": "Workflow",
        "title": "Choosing the mode to open a ZipFile in",
        "concepts": ["CreateZip", "AppendToZip"],
        "also_from": ["WritingZip", "ZipArchives"],
        "read_from": "chapter 11, the writing zip section: zipfile.ZipFile opens in mode 'w', which erases an "
                     "existing archive and starts fresh, mode 'a', which keeps what is already there and adds to "
                     "it, or mode 'x', which refuses to touch a file that already exists",
        "why": "the explanations describe what a programmer decides when zipfile.ZipFile is called - should an "
               "existing archive of the same name be kept, erased, or left untouched with an error raised instead "
               "- with a different mode chosen on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "A ZipFile is opened with a mode"},
                {"id": "exists", "label": "This ZIP file already exists", "kind": "decision"},
                {"id": "wnew", "label": "Mode 'w' creates a new ZIP file, erasing one that exists"},
                {"id": "amode", "label": "Mode 'a' adds files and keeps what is there"},
                {"id": "xmode", "label": "Mode 'x' refuses an existing file with FileExistsError"},
            ],
            "flows": [["start", "need"], ["need", "exists"], ["exists", "wnew", "no"], ["exists", "amode", "add"],
                      ["exists", "xmode", "refuse"], ["wnew", "end"], ["amode", "end"], ["xmode", "end"]],
        },
    },
    {
        "id": "ArchiveFromCreatedToExtracted",
        "pattern": "LifeCycle",
        "title": "A ZIP archive's life from created to extracted",
        "concepts": ["CreateZip", "AppendToZip", "NameList", "ExtractAll"],
        "also_from": ["WritingZip", "ReadingZip", "ExtractingZip", "ZipArchives"],
        "read_from": "chapter 11, the writing, reading and extracting zip sections: mode 'w' creates the archive, "
                     "write adds files to it, a with statement closes that use, a later open in mode 'a' can add "
                     "more, namelist reads an archive's own member names, and extractall takes every member back "
                     "out",
        "why": "the explanations describe the states one archive passes through on its way from being created to "
               "being extracted - created, filled by write, closed, reopened for reading, and extracted - and the "
               "operation that moves it from one state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "created", "label": "Created: mode 'w' creates the archive, erasing one that exists"},
                {"id": "filled", "label": "Filled: write adds a file to the archive from the disk"},
                {"id": "closed", "label": "Closed: a with statement closes the archive"},
                {"id": "extracted", "label": "Extracted: extractall extracts every member into a target folder"},
            ],
            "initial": "created",
            "final": ["extracted"],
            "transitions": [
                ["created", "filled", "write adds a file to the archive"],
                ["filled", "filled", "write adds a file to the archive"],
                ["filled", "closed", "a with statement closes the archive"],
                ["closed", "filled", "mode 'a' adds files and keeps what is there"],
                ["closed", "extracted", "extractall extracts every member into a target folder"],
            ],
        },
    },
    {
        "id": "BackupProjectRoundTrip",
        "pattern": "Interaction",
        "title": "The backup project's own exchange between program and archive",
        "concepts": ["NextZipName", "WalkIntoZip", "ArchiveNames"],
        "also_from": ["ZipNaming", "ZipBuilding", "BackupProject"],
        "read_from": "chapter 11, the backup project's own zip naming and zip building sections: the program "
                     "works out the next unused archive name, opens a new ZipFile under that name, walks the "
                     "folder and writes each file into the archive under its own path",
        "why": "the passage is an exchange between parties in an order that matters - the program works out a "
               "name, opens the archive under it, walks the folder, writes each file in turn, and ends with one "
               "detail about what the walk leaves out - an interaction",
        "data": {
            "participants": [
                {"id": "program", "label": "The backup program"},
                {"id": "archive", "label": "The new ZIP archive on disk"},
            ],
            "messages": [
                ["program", "archive", "the program works out the name from the folder and a growing number"],
                ["program", "archive", "ZipFile opens the archive under that name in write mode"],
                ["program", "archive", "the program walks the folder and writes each file it finds"],
                ["program", "archive", "the program prints Adding file, then Done"],
                ["archive", "program", "an empty folder with no files is never recorded in the archive", "reply"],
            ],
        },
    },
    {
        "id": "PracticeProgramUses",
        "pattern": "SetOfUses",
        "title": "What the chapter's own four practice programs let a program do",
        "concepts": ["SelectiveCopy", "LargeFiles", "RenumberFiles", "DateRenaming"],
        "also_from": ["Programs", "PracticeWork"],
        "read_from": "chapter 11, the practice programs section: the four programs walk a tree and copy files of "
                     "one extension, walk a tree and print files above a size limit, close gaps in a run of "
                     "numbered file names, and swap the month and the day inside a dated file name",
        "why": "the passage lists what each of the four programs does to a tree of files it walks - copy by "
               "extension, print by size, renumber, and swap a date - a set of uses of the chapter's own walking "
               "and renaming tools, not a sequence one leads into the next",
        "data": {
            "system": "THE CHAPTER'S OWN FOUR PRACTICE PROGRAMS",
            "actors": [{"id": "walk", "label": "os.walk, the tree-walking loop every program shares"}],
            "usecases": [
                {"id": "copy", "label": "Copy every file of one chosen extension into a new folder"},
                {"id": "size", "label": "Print every file whose size passes a limit, found with os.path.getsize"},
                {"id": "renumber", "label": "Close the gaps in a run of numbered file names"},
                {"id": "date", "label": "Swap the month and the day inside a file name's own date"},
            ],
            "links": [["walk", "copy"], ["walk", "size"], ["walk", "renumber"], ["walk", "date"]],
        },
    },
    {
        "id": "OrganizingFilesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Organizing files at a glance: five branches",
        "concepts": ["CopyingAndMoving", "Deleting", "FolderTrees", "ZipArchives", "BackupProject"],
        "also_from": ["Copying", "Moving", "PermanentDeletion", "SaferDeletion", "Listing", "Walking",
                       "WritingZip", "ReadingZip", "ExtractingZip", "ArchiveHelpers", "ZipNaming", "ZipBuilding"],
        "read_from": "chapter 11, the opening of each of its five main branches: shutil copies and moves files "
                     "and folders, os and shutil delete them permanently or safely, os.walk and pathlib walk a "
                     "whole folder tree, zipfile creates reads and extracts archives, and the backup project "
                     "walks a folder into a numbered archive",
        "why": "the section classifies one topic, organizing files, by what each branch is about and lists "
               "examples under each - a topic and its parts, laid out to remember, with the one idea that holds "
               "for every part stated once at the root",
        "data": {
            "root": "A program copies, deletes, walks and archives files and folders",
            "branches": [
                {"label": "Copying and moving: shutil relocates files and folders",
                 "children": ["shutil.copy copies a file and keeps the source in place",
                              "shutil.copytree copies a whole folder with everything in it",
                              "shutil.move moves a file or folder and removes the source"]},
                {"label": "Deleting: permanent functions, and two ways to stay safe",
                 "children": ["os.unlink and os.rmdir delete a file or an empty folder for good",
                              "shutil.rmtree deletes a whole folder tree for good",
                              "a dry run previews a delete, copy or move before it actually runs"]},
                {"label": "Folder trees: listing one folder, walking a whole tree",
                 "children": ["os.listdir and Path.iterdir list the names inside one folder",
                              "a glob pattern matches file names with a small wildcard language",
                              "os.walk visits a folder and every folder below it in turn"]},
                {"label": "Zip archives: zipfile creates, reads and extracts",
                 "children": ["a ZipFile opened in mode w, a or x writes or adds to an archive",
                              "namelist and getinfo read a member's own name and size",
                              "extractall and extract take files back out of the archive"]},
                {"label": "Backup project: walking a folder into a numbered archive",
                 "children": ["the program works out the next unused archive name",
                              "it walks the folder and writes each file it finds into the archive"]},
            ],
        },
    },
]

STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then".split())


def _labels(d):
    """every element label of a diagram, whatever its type"""
    x = d["data"]; out = []
    for n in x.get("nodes", []) + x.get("states", []) + x.get("actors", []) + x.get("usecases", []) + x.get("participants", []):
        out.append(n["label"] if isinstance(n, dict) else n)
    out += [f[2] for f in x.get("flows", []) + x.get("transitions", []) if len(f) > 2 and f[2]]
    out += [m[2] for m in x.get("messages", [])]
    for b in x.get("branches", []):
        out.append(b["label"]); out += b.get("children", [])
    if x.get("root"): out.append(x["root"])
    if x.get("system"): out.append(x["system"])
    return out


def grounding(d, nodes):
    """share of a diagram's content words that occur in the explanations of its concepts (and their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join(_labels(d)).lower()) if w not in STOP and len(w) > 1]
    hit = [w for w in words if w in text or w.rstrip("s") in text or (w + "s") in text]
    return len(hit), len(words), sorted(set(w for w in words if w not in hit))


def run_checks(nodes=None, mapping=None):
    """structural rules and, with the chapter's nodes, the grounding ratio; with the CME mapping, the pattern is known and its type is assigned"""
    bad = []
    ids = [d["id"] for d in DIAGRAMS]
    if len(ids) != len(set(ids)): bad.append("duplicate diagram ids")
    by = {n["id"]: n for n in nodes} if nodes else None
    for d in DIAGRAMS:
        for f in ("pattern", "title", "concepts", "read_from", "why", "data"):
            if not d.get(f): bad.append("%s: missing %s" % (d["id"], f))
        if by:
            for c in d["concepts"] + d.get("also_from", []):
                if c not in by: bad.append("%s: unknown concept %s" % (d["id"], c))
        if mapping:
            m = mapping.get(d["pattern"])
            if not m: bad.append("%s: pattern %s is not in the CME mapping" % (d["id"], d["pattern"]))
            else:
                d["type"] = m["types"][0]
        x = d["data"]
        if "flows" in x:
            nid = set(n["id"] for n in x["nodes"]) | {"start", "end"}
            for f in x["flows"]:
                if f[0] not in nid or f[1] not in nid: bad.append("%s: flow names an unknown node %r" % (d["id"], f))
            if not any(f[0] == "start" for f in x["flows"]) or not any(f[1] == "end" for f in x["flows"]): bad.append("%s: no start or no end" % d["id"])
            for n in x["nodes"]:
                if n.get("kind") == "decision" and len([f for f in x["flows"] if f[0] == n["id"]]) < 2: bad.append("%s: decision %s has fewer than two outgoing flows" % (d["id"], n["id"]))
        if "transitions" in x:
            sid = set(s["id"] if isinstance(s, dict) else s for s in x["states"])
            if x["initial"] not in sid: bad.append("%s: initial state unknown" % d["id"])
            for f in x.get("final", []):
                if f not in sid: bad.append("%s: final state unknown" % d["id"])
            for tr in x["transitions"]:
                if tr[0] not in sid or tr[1] not in sid or not tr[2]: bad.append("%s: transition %r unknown state or unlabelled" % (d["id"], tr))
        if "usecases" in x:
            aid = set(a["id"] for a in x["actors"]); uid = set(u["id"] for u in x["usecases"])
            for a, u in x["links"]:
                if a not in aid or u not in uid: bad.append("%s: link %r names an unknown actor or use case" % (d["id"], (a, u)))
            if uid - set(u for _, u in x["links"]): bad.append("%s: a use case has no actor" % d["id"])
        if "messages" in x:
            pid = set(p["id"] for p in x["participants"])
            for m in x["messages"]:
                if m[0] not in pid or m[1] not in pid or not m[2]: bad.append("%s: message %r unknown participant or empty" % (d["id"], m))
        if "branches" in x:
            if len(x["branches"]) < 2: bad.append("%s: a mind map needs at least two branches" % d["id"])
        for lab in _labels(d):
            if len(lab) > 72: bad.append("%s: label over 72 characters: %r" % (d["id"], lab))
        if nodes:
            h, n, miss = grounding(d, nodes)
            d["grounding"] = [h, n]
            if n and h / n < 0.8: bad.append("%s: grounding %d/%d below 0.8; words not in the concepts' explanations: %s" % (d["id"], h, n, ", ".join(miss)))
    return bad


if __name__ == "__main__":
    import sys, json, glob, os
    here = os.path.dirname(os.path.abspath(__file__))
    f = sorted(glob.glob(os.path.join(here, "ch11-page", "page_data_v*.json")))
    if not f:
        print("no page_data yet; run sen0414_page_data first"); sys.exit(2)
    nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-24s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
