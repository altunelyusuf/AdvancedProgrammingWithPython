#!/usr/bin/env python3
"""SEN0414, chapter 10 (Reading and Writing Files, Automate the Boring Stuff with Python, 3rd edition) - the
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
sen0414_ch09_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of
another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ChoosingAPathOperation",
        "pattern": "Workflow",
        "title": "What kind of thing a path operation does",
        "concepts": ["PathConstruction", "PathDerivation", "PathValidity", "MakingFolders"],
        "also_from": ["PathObjects", "DerivedPaths", "FileInformation", "CreatingFolders", "Filepaths", "Folders"],
        "read_from": "chapter 10, the filepaths and folders sections: Path() joins names into a path object without touching a disk, with_suffix and relative_to build a new path the same way, exists and is_file ask the file system a question without changing anything, and mkdir and makedirs create a folder on disk",
        "why": "the explanations describe what a programmer decides, in order, when one line of code calling a path method is written - does it only compute a new path object, does it only ask the file system a question, or does it change a file or folder on disk - with a different answer reached on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "A line of code calls a method on a path or a folder"},
                {"id": "changes", "label": "Does the call change a file or folder on disk?", "kind": "decision"},
                {"id": "mkdir", "label": "mkdir and os.makedirs create a folder on disk"},
                {"id": "asks", "label": "Does the call ask the file system a question?", "kind": "decision"},
                {"id": "exists", "label": "exists, is_file and is_dir ask the file system a question"},
                {"id": "compute", "label": "with_suffix, with_name and relative_to build a new path, no disk used"},
                {"id": "join", "label": "Path() joins names into a path object without touching a disk"},
            ],
            "flows": [["start", "need"], ["need", "changes"], ["changes", "mkdir", "yes"],
                      ["changes", "asks", "no"], ["asks", "exists", "yes"], ["asks", "compute", "no"],
                      ["compute", "join"], ["mkdir", "end"], ["exists", "end"], ["join", "end"]],
        },
    },
    {
        "id": "ChoosingAnOpenMode",
        "pattern": "Workflow",
        "title": "Choosing the mode to open a file in",
        "concepts": ["OpenAndModes", "PlainVersusBinaryFiles"],
        "also_from": ["OpenedFiles", "WholeFileMethods", "TextFiles"],
        "read_from": "chapter 10, the opened files and whole file methods sections: open() reads in mode r by default, writes after emptying the file in mode w, appends in mode a, and creates a new file and fails if it exists in mode x, and text or binary data decides whether the file is opened in text or binary mode",
        "why": "the explanations describe what a programmer decides, in order, when open() is called - is the file read or written, should an existing file be emptied or kept, and is the data text or binary - with a different mode chosen on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "A file is about to be opened with open() or a whole file method"},
                {"id": "binary", "label": "Is the file binary, not plain text characters?", "kind": "decision"},
                {"id": "bmode", "label": "binary mode reads and writes bytes, not text"},
                {"id": "write", "label": "Is the file opened to write, not to read?", "kind": "decision"},
                {"id": "existing", "label": "Does the mode overwrite the file, or append to the end of it?", "kind": "decision"},
                {"id": "wmode", "label": "Mode w overwrites the file, created if not already there"},
                {"id": "amode", "label": "Mode a appends to the end of it, created if not already there"},
                {"id": "rmode", "label": "Mode r reads the file, the default mode of open()"},
            ],
            "flows": [["start", "need"], ["need", "binary"], ["binary", "bmode", "yes"], ["binary", "write", "no"],
                      ["write", "existing", "yes"], ["write", "rmode", "no"], ["existing", "wmode", "yes"],
                      ["existing", "amode", "no"], ["bmode", "end"], ["rmode", "end"], ["wmode", "end"],
                      ["amode", "end"]],
        },
    },
    {
        "id": "FileFromOpenToClosed",
        "pattern": "LifeCycle",
        "title": "A file object's life from opened to closed",
        "concepts": ["OpenAndModes", "WriteMethod", "ReadMethods", "CloseMethod", "WithStatement", "ClosedFileError"],
        "also_from": ["OpenedFiles", "AutomaticClosing"],
        "read_from": "chapter 10, the opened files and automatic closing sections: open() returns a file object; write() and read() act on it while it is open; close() ends its use, and a with statement closes it automatically on every way out of its block; a closed file object raises ValueError if it is read or written again",
        "why": "the explanations describe the states one file object passes through on its way from being opened to being closed - opened, written or read, then closed - and the operation that moves it from one state to the next, including the with statement's own automatic move to closed: a life cycle",
        "data": {
            "states": [
                {"id": "opened", "label": "Opened: open() returns a file object in the mode it was given"},
                {"id": "active", "label": "Active: write() or read() acts on the open file object"},
                {"id": "closed", "label": "Closed: close() ends the file object's use"},
            ],
            "initial": "opened",
            "final": ["closed"],
            "transitions": [
                ["opened", "active", "write() or read() is called on the file object"],
                ["active", "active", "another write() or read() is called on the same open file object"],
                ["active", "closed", "close() is called, or a with statement's block ends"],
                ["opened", "closed", "a with statement's block ends with nothing written or read"],
                ["closed", "closed", "a read or write on the closed file object raises ValueError"],
            ],
        },
    },
    {
        "id": "ShelfRoundTrip",
        "pattern": "Interaction",
        "title": "A value's round trip through a shelf",
        "concepts": ["ShelveOpen", "ShelfAsDictionary", "ShelfWriteback"],
        "also_from": ["Shelves", "SavedData"],
        "read_from": "chapter 10, the shelves section: shelve.open() opens a shelf like a dictionary, a value is stored under a key and the shelf is closed, and a later shelve.open() of the same file reads the value back by the same key, though a shelf cannot see a mutable value changed in place unless it is assigned back or writeback is used",
        "why": "the passage is an exchange between parties in an order that matters - a value is stored under a key, the shelf is closed, the shelf is reopened, and the same key reads the value back - an interaction",
        "data": {
            "participants": [
                {"id": "program", "label": "The Python program"},
                {"id": "shelf", "label": "The shelf file on disk"},
            ],
            "messages": [
                ["program", "shelf", "shelve.open() opens the shelf file, creating it if it does not exist"],
                ["program", "shelf", "a value is stored under a string key, like a dictionary"],
                ["program", "shelf", "close() ends the shelf's use and writes it to disk"],
                ["program", "shelf", "a later shelve.open() of the same file opens it again"],
                ["shelf", "program", "the same key reads the stored value back", "reply"],
            ],
        },
    },
    {
        "id": "QuizGeneratorUses",
        "pattern": "SetOfUses",
        "title": "What Project 4's quiz generator lets a user do",
        "concepts": ["QuizData", "QuizFiles", "QuizOutputDiffers"],
        "also_from": ["QuizProgram", "ChapterPrograms"],
        "read_from": "chapter 10, the quiz program section: the program keeps the states and capitals in a dictionary, shuffles the states and the wrong answers, writes a quiz file and an answer key file for each quiz, and a student who takes the quiz can be marked against the answer key",
        "why": "the passage lists what the program and a person each do with the files it writes - keep the data, shuffle the order, write a quiz file, write an answer key file, take the quiz, mark it against the key - a set of uses by actors, not a sequence",
        "data": {
            "system": "PROJECT 4'S QUIZ GENERATOR",
            "actors": [{"id": "program", "label": "Quiz generator program"}, {"id": "student", "label": "Student"}],
            "usecases": [
                {"id": "keep", "label": "Keep the 50 states and their capitals in a dictionary"},
                {"id": "shuffle", "label": "Shuffle the order of the states for each quiz"},
                {"id": "wrong", "label": "Choose three wrong capitals at random for each question"},
                {"id": "writequiz", "label": "Write a quiz file with a header and four lettered options per question"},
                {"id": "writekey", "label": "Write an answer key file naming the correct letter for each question"},
                {"id": "take", "label": "Read and answer a quiz file"},
                {"id": "mark", "label": "Mark a taken quiz against its answer key file"},
            ],
            "links": [["program", "keep"], ["program", "shuffle"], ["program", "wrong"], ["program", "writequiz"],
                      ["program", "writekey"], ["student", "take"], ["student", "mark"]],
        },
    },
    {
        "id": "FilesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Reading and writing files at a glance: four branches",
        "concepts": ["Filepaths", "Folders", "TextFiles", "SavedData"],
        "also_from": ["PathObjects", "WorkingLocations", "PathAnatomy", "CreatingFolders", "FindingFiles",
                       "FileInformation", "WholeFileMethods", "OpenedFiles", "TextEncoding", "AutomaticClosing",
                       "Shelves", "PlainAlternative"],
        "read_from": "chapter 10, the opening of each of its four main branches: a path names where a file lies, a folder is created and searched, a text file is read and written whole or opened as a file object, and saved data outlives the program in a shelf or a json file",
        "why": "the section classifies one topic, reading and writing files, by what each branch is about and lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for every part stated once at the root",
        "data": {
            "root": "A program builds a path, acts on a folder, and reads or writes a file",
            "branches": [
                {"label": "Filepaths: the chapter builds the name of a file",
                 "children": ["Path() joins the names it is given into one path object",
                              "working directory and home directory are folders a program carries",
                              "a path breaks apart into pieces named stem and suffix"]},
                {"label": "Folders: the chapter acts on a folder",
                 "children": ["the chapter makes a new folder in one of two ways",
                              "a glob pattern, built from a small language, lists a folder's files",
                              "the program asks the file system whether a path exists"]},
                {"label": "Text files: the chapter reads and writes file content",
                 "children": ["read_text and write_text open, act on, and close a file in one call",
                              "open returns a file object read from and written to by hand",
                              "the encoding argument decides how characters become bytes on disk",
                              "the with statement closes a file on every way out of its block"]},
                {"label": "Saved data: a program's variables outlive the program",
                 "children": ["a shelf behaves like a dictionary whose keys and values survive",
                              "a plain format keeps data as text any program can read",
                              "shelve opens a binary file on disk and makes it behave like a dictionary"]},
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
    f = sorted(glob.glob(os.path.join(here, "ch10-page", "page_data_v*.json")))
    if not f:
        print("no page_data yet; run sen0414_page_data first"); sys.exit(2)
    nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-24s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
