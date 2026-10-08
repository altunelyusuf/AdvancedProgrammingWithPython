#!/usr/bin/env python3
"""SEN0414, chapter 7 (Dictionaries and Structuring Data, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of
a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative
pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is
reused by every course. Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as (the
diagram type follows from the mapping, never from the author), the passage it was read from (also_from names further concepts whose
explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the element names the
renderer of that type expects. Every element label is made of words that occur in the explanations of the accompanying concepts or their
section; run_checks() measures that (the grounding ratio) besides the structural rules. This module follows the layout of
sen0414_ch05_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ReadingAKey",
        "pattern": "Workflow",
        "title": "Choosing how to read a key from a dictionary",
        "concepts": ["MembershipOnKeys", "GetMethod", "SetdefaultMethod", "KeyErrorOnMissing"],
        "also_from": ["Reading", "AbsentKeys", "ReadingAndChanging", "KeyRules", "BirthdayLookup"],
        "read_from": "chapter 7, the Reading a pair and Absent keys sections: the in test asks whether a key is present, the get method returns the value or a fallback without changing the dictionary, the setdefault method stores a default only if the key is not there and returns the value now stored, and the subscript raises KeyError when the key is absent",
        "why": "the explanations describe what the programmer decides in order - does the key have to be there, is a fallback enough, must the key exist afterwards - with a different tool on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "The program reads the value of a key that may be absent"},
                {"id": "error", "label": "Is the absent key an error in the data?", "kind": "decision"},
                {"id": "subscript", "label": "Use square brackets: KeyError names the missing key"},
                {"id": "branch", "label": "Must the program branch on whether the key is present?", "kind": "decision"},
                {"id": "intest", "label": "Test with the in operator: the keys are asked, no error is raised"},
                {"id": "after", "label": "Must the key exist in the dictionary afterwards?", "kind": "decision"},
                {"id": "setdefault", "label": "Call setdefault: it stores the key if absent and returns the value"},
                {"id": "get", "label": "Call get with a fallback: the dictionary is not changed"},
            ],
            "flows": [["start", "need"], ["need", "error"], ["error", "subscript", "yes"], ["error", "branch", "no: the key may be absent"], ["branch", "intest", "yes"], ["branch", "after", "no"], ["after", "setdefault", "yes"], ["after", "get", "no"], ["subscript", "end"], ["intest", "end"], ["setdefault", "end"], ["get", "end"]],
        },
    },
    {
        "id": "LifeOfAPair",
        "pattern": "LifeCycle",
        "title": "The life of a key-value pair in a dictionary",
        "concepts": ["AddOrReplacePair", "DeletePair", "PopMethod", "KeyValuePair"],
        "also_from": ["Changing", "InsertionOrder", "KeyErrorOnMissing", "UpdateAndMerge"],
        "read_from": "chapter 7, the Adding, replacing and removing section: assignment with square brackets adds a pair when the key is new and replaces the value when the key exists, the del statement removes a pair and raises KeyError when the key is not present, and the pop method removes a pair and returns its value",
        "why": "the explanations describe the states a pair is in - not in the dictionary, present with a value, present with a replaced value, removed - and the operations that move it from one state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "absent", "label": "Absent: the key is not in the dictionary"},
                {"id": "present", "label": "Present: the key is stored with its value"},
                {"id": "replaced", "label": "Replaced: the same key now stands for a new value"},
                {"id": "removed", "label": "Removed: the pair is deleted and the key is absent again"},
            ],
            "initial": "absent",
            "final": ["removed"],
            "transitions": [["absent", "present", "assignment to a new key adds a pair at the end"], ["present", "replaced", "assignment to the same key replaces the value"], ["replaced", "replaced", "another assignment replaces the value again"], ["present", "removed", "the del statement or the pop method removes the pair"], ["replaced", "removed", "the del statement or the pop method removes the pair"], ["absent", "absent", "del on an absent key raises KeyError"]],
        },
    },
    {
        "id": "HashedLookup",
        "pattern": "Interaction",
        "title": "How a dictionary finds the value of a key",
        "concepts": ["HashValue", "HashableKeys", "KeyErrorOnMissing", "KeyValuePair"],
        "also_from": ["WhatMayBeAKey", "KeyRules", "AbsentKeys", "EqualKeysShareASlot"],
        "read_from": "chapter 7, the Keys and hashing section: Python turns the key into a number by a rule, uses that number to decide where the pair is kept, compares the key it finds there with the key asked for, and returns the value or raises KeyError; a list cannot be a key because its hash value would change",
        "why": "the passage is an exchange between parties in an order that matters - the program asks, the dictionary computes the hash, the table answers with a stored pair, the keys are compared and the value or the error is returned: an interaction",
        "data": {
            "participants": [{"id": "program", "label": "Program"}, {"id": "dict", "label": "Dictionary"}, {"id": "hash", "label": "Hash value"}, {"id": "table", "label": "Stored pairs"}],
            "messages": [
                ["program", "dict", "asks for the value of the key 'color'"],
                ["dict", "hash", "asks for the hash value of the key"],
                ["hash", "dict", "returns a whole number computed from the key", "reply"],
                ["dict", "table", "uses the number to find where the pair is stored"],
                ["table", "dict", "returns the stored key and value found there, if any", "reply"],
                ["dict", "dict", "compares the stored key with the key asked for"],
                ["dict", "program", "returns the value when the keys are equal", "reply"],
                ["dict", "program", "raises KeyError when no equal key is there", "reply"],
                ["program", "dict", "a list as a key has no hash value that stays the same"],
            ],
        },
    },
    {
        "id": "CountingByKey",
        "pattern": "Workflow",
        "title": "Counting the items of a sequence with a dictionary",
        "concepts": ["CharacterCount", "CounterClass", "DefaultdictCounting"],
        "also_from": ["Counting", "CountingAndGrouping", "SetdefaultMethod", "GetMethod", "KeyErrorOnMissing"],
        "read_from": "chapter 7, the Setting default values section and the character count program: the loop takes each character, setdefault makes sure the key exists starting at 0, and one is added to the count; the Counter class and the defaultdict class give the same result in less code",
        "why": "the explanations describe the steps the program repeats for every item - take the item, make sure its key exists with the count 0, add one - and the choice of tool that shortens them: a workflow with a loop and a decision",
        "data": {
            "nodes": [
                {"id": "empty", "label": "Start with an empty dictionary of counts"},
                {"id": "more", "label": "Does the message have more characters?", "kind": "decision"},
                {"id": "take", "label": "Take one character of the message"},
                {"id": "exists", "label": "Make sure the key exists with the starting value 0"},
                {"id": "add", "label": "Add one to the count of that character"},
                {"id": "print", "label": "The dictionary of counts is the result"},
                {"id": "shorter", "label": "Is the Counter class wanted?", "kind": "decision"},
                {"id": "counter", "label": "Use the Counter class: one call counts the whole message"},
            ],
            "flows": [["start", "empty"], ["empty", "shorter"], ["shorter", "counter", "yes"], ["shorter", "more", "no: the loop of the book"], ["counter", "print"], ["more", "take", "yes"], ["more", "print", "no"], ["take", "exists"], ["exists", "add"], ["add", "more"], ["print", "end"]],
        },
    },
    {
        "id": "ChessboardUses",
        "pattern": "SetOfUses",
        "title": "What the chessboard simulator lets its user do",
        "concepts": ["ChessboardCommands", "ChessboardModel", "ChessboardPrinter"],
        "also_from": ["Modelling", "AddOrReplacePair", "DeletePair", "BoardTemplate", "StructuringData", "StarSyntax"],
        "read_from": "chapter 7, the Interactive Chessboard Simulator project: the user types move, remove, set, reset, clear, fill or quit, the program changes the dictionary that holds the pieces, and after each command the printing function draws the board from the template",
        "why": "the passage lists what the user and the program do with the chessboard dictionary - move a piece, remove it, set a square, reset or clear the board, fill it, see the board drawn - a set of uses by actors, not a sequence",
        "data": {
            "system": "THE CHESSBOARD SIMULATOR",
            "actors": [{"id": "user", "label": "Player"}, {"id": "program", "label": "Chessboard program"}],
            "usecases": [
                {"id": "move", "label": "Move the piece at e2 to e4"},
                {"id": "remove", "label": "Remove the piece at a square from the board"},
                {"id": "set", "label": "Set a square to a piece, such as a white pawn"},
                {"id": "reset", "label": "Reset the pieces to the starting position"},
                {"id": "clear", "label": "Clear the board"},
                {"id": "fill", "label": "Fill the board with white pawns"},
                {"id": "quit", "label": "Quit the program"},
                {"id": "draw", "label": "Draw the board from the template after every command"},
                {"id": "split", "label": "Split the line into a list of words with split()"},
            ],
            "links": [["user", "move"], ["user", "remove"], ["user", "set"], ["user", "reset"], ["user", "clear"], ["user", "fill"], ["user", "quit"], ["program", "draw"], ["program", "split"]],
        },
    },
    {
        "id": "DictionaryAtAGlance",
        "pattern": "TopicAndParts",
        "title": "A dictionary at a glance: what it is made of and what it can do",
        "concepts": ["DictionaryType", "KeyValuePair", "HashableKeys", "KeysValuesItems", "NestedDictionaries"],
        "also_from": ["PairsAndMappings", "DictionaryModel", "ListContrast", "KeyRules", "Views", "Nesting", "InsertionOrder", "KeysNotIndexes", "TupleAsKey"],
        "read_from": "chapter 7, the opening sections: a dictionary is a mutable collection of key-value pairs written in curly brackets, the keys must be hashable, it differs from a list in having keys and not indexes, the methods keys, values and items return views, and values may themselves be dictionaries",
        "why": "the section classifies one topic, the dictionary, by what it is made of, by the rule for its keys, by how it differs from a list and by the ways of reading it, and lists the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "The dictionary: a mutable collection of key-value pairs",
            "branches": [
                {"label": "What it is made of: key-value pairs", "children": ["Curly brackets with a key and a value in each pair", "Values of any type, including other dictionaries", "Each key occurs only once", "Pairs kept in the order of insertion"]},
                {"label": "What may be a key: a hashable value", "children": ["Strings, numbers and tuples are hashable", "Lists and dictionaries are unhashable", "A tuple replaces a list as a key"]},
                {"label": "How it differs from a list", "children": ["Keys instead of indexes", "Equality that ignores the order of the pairs", "A mapping and not a sequence: no slicing"]},
                {"label": "How it is read: the three views", "children": ["keys() gives the keys", "values() gives the values", "items() gives the key-value pairs"]},
            ],
        },
    },
    {
        "id": "CopyingChoices",
        "pattern": "TopicAndParts",
        "title": "Three ways to copy a nested dictionary",
        "concepts": ["CopyingDictionaries", "NestedDictionaries", "ChessboardModel"],
        "also_from": ["Nesting", "TotalBrought", "StructuringData"],
        "read_from": "chapter 7, the Nested Dictionaries and Lists section and the chessboard reset: an assignment makes a second name for the same dictionary, copy.copy makes a new outer dictionary that shares the inner ones, and copy.deepcopy copies every level; the chessboard resets with copy.copy of the starting pieces",
        "why": "the passage lists the choices open to the programmer when a nested dictionary must be copied - an alias, a shallow copy, a deep copy - and what each shares with the original: a topic and its parts, laid out to choose between",
        "data": {
            "root": "Copying a nested dictionary: which objects stay the same",
            "branches": [
                {"label": "An alias: no copy at all", "children": ["A second name for the same dictionary", "Every change is seen under both names"]},
                {"label": "A shallow copy: copy.copy", "children": ["A new outer dictionary", "The inner dictionaries are the same objects", "Used for the chessboard, whose values are strings"]},
                {"label": "A deep copy: copy.deepcopy", "children": ["New copies at every level", "A change to the original does not reach the copy", "Copies every level of the structure"]},
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
    import sys, json, glob, os, re
    here = os.path.dirname(os.path.abspath(__file__))
    nodes = None
    f = glob.glob(os.path.join(here, "ch07-page", "page_data_v9_27_0.json"))   # the page data of this build (older files in the folder are of the older standard)
    if f:
        nodes = json.load(open(f[0]))["nodes"]
    else:                                   # before the page data exists: the nodes of the corpus, with the same fields
        sys.path.insert(0, here)
        import sen0414_ch07_corpus_v1_0_0 as C
        nodes = [{"id": n[0], "label": n[1], "parent": n[3], "body": C.facet_text(n[5]), "definition": n[4][1] if n[4] else ""} for n in C.NODES]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
