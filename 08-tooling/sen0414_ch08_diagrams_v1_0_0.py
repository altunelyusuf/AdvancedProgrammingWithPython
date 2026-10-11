#!/usr/bin/env python3
"""SEN0414, chapter 8 (Manipulating Strings, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of
the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case
diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts
whose explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects. Every element label is made of words that occur in the explanations of
the accompanying concepts or their section; run_checks() measures that (the grounding ratio) besides the structural rules.
This module follows the layout of sen0414_ch07_diagrams_v1_0_0.py (the helper functions below are the same rules, written
again because a file of another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ChoosingAQuote",
        "pattern": "Workflow",
        "title": "Choosing how to write a literal that needs a quote mark",
        "concepts": ["QuoteStyles", "EscapeSequences", "StringPrefixes", "RawStrings"],
        "also_from": ["StringQuoting", "LiteralForms", "StringLiterals", "UnrecognizedEscapes"],
        "read_from": "chapter 8, the string quoting and literal forms sections: a literal may begin and end with single or double quotes, an escape sequence puts a hard-to-type character inside a literal, a raw string reads every backslash as an ordinary character, and a letter prefix changes how the whole literal is read",
        "why": "the explanations describe what the programmer decides in order when a literal needs an apostrophe, a backslash or a Windows path - does the other quote avoid the problem, is an escape needed, is the text a path or a pattern that wants every backslash kept - with a different choice on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "The literal needs an apostrophe or a backslash inside it"},
                {"id": "apostrophe", "label": "Does the literal need an apostrophe or a double quote?", "kind": "decision"},
                {"id": "otherquote", "label": "Choose the other quote style; the character becomes ordinary"},
                {"id": "path", "label": "Is the text a Windows path or a pattern full of backslashes?", "kind": "decision"},
                {"id": "raw", "label": "Write a raw string with the r prefix; every backslash is kept"},
                {"id": "escape", "label": "Write an escape sequence such as the quote escape or a tab"},
                {"id": "check", "label": "Does the backslash form a recognised escape sequence?", "kind": "decision"},
                {"id": "warn", "label": "An unrecognized escape keeps the backslash and draws a SyntaxWarning"},
            ],
            "flows": [["start", "need"], ["need", "apostrophe"], ["apostrophe", "otherquote", "yes"], ["apostrophe", "path", "no"], ["path", "raw", "yes"], ["path", "escape", "no"], ["escape", "check"], ["check", "otherquote", "yes: use the escape"], ["check", "warn", "no"], ["otherquote", "end"], ["raw", "end"], ["warn", "end"]],
        },
    },
    {
        "id": "StringEditJourney",
        "pattern": "LifeCycle",
        "title": "A piece of text's life from literal to bytes",
        "concepts": ["StringImmutability", "Concatenation", "ChangingCase", "Utf8Encoding"],
        "also_from": ["StringAccess", "StringMethods", "CharactersAndBytes", "StringFormatting"],
        "read_from": "chapter 8, the string properties, string formatting, text case and text encodings sections: a string cannot be changed in place, a new string is built with concatenation or a method such as upper, and the finished text is turned into bytes by an encoding such as utf-8",
        "why": "the explanations describe the states a piece of text passes through on its way from source code to bytes - written as a literal, rebuilt by a method into another string, joined with other text, finally encoded - and the operation that moves it from one state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "literal", "label": "Literal: the text is a string literal"},
                {"id": "rebuilt", "label": "Converted: upper() or lower() returns a new string"},
                {"id": "joined", "label": "Joined: concatenation with plus joins text"},
                {"id": "bytes", "label": "Encoded: utf-8 turns the characters into bytes"},
            ],
            "initial": "literal",
            "final": ["bytes"],
            "transitions": [["literal", "rebuilt", "the upper method is called, which returns a new string"], ["rebuilt", "rebuilt", "another method is called on the new string"], ["literal", "joined", "the plus operator joins the literal with other text"], ["rebuilt", "joined", "the new string is joined with other text"], ["joined", "bytes", "encode turns the text into bytes"], ["literal", "bytes", "a literal is encoded directly, with no method called first"]],
        },
    },
    {
        "id": "ResolvingAField",
        "pattern": "Interaction",
        "title": "How an f-string resolves one field",
        "concepts": ["FStrings", "FormatSpecifiers", "DebugAndConversions"],
        "also_from": ["FormatInterpolation", "StringFormatting", "FormatMethod"],
        "read_from": "chapter 8, the format interpolation section: an expression inside curly brackets is evaluated, the value is formatted by format, a specifier after a colon controls width and precision, and a conversion such as !r chooses str, repr or ascii before the specifier is applied",
        "why": "the passage is an exchange between parties in an order that matters - the literal names an expression, the expression is evaluated, a conversion and a specifier are applied, and the formatted text is substituted back into the string: an interaction",
        "data": {
            "participants": [{"id": "fstring", "label": "The f-string literal"}, {"id": "expr", "label": "The expression inside the curly brackets"}, {"id": "spec", "label": "A format specifier after a colon"}, {"id": "value", "label": "The value"}],
            "messages": [
                ["fstring", "expr", "the expression inside a pair of curly brackets is evaluated"],
                ["expr", "value", "the value is placed into the text at that point", "reply"],
                ["fstring", "spec", "a colon introduces a format specifier that controls width and precision"],
                ["spec", "value", "the value is formatted by the built-in format function", "reply"],
                ["value", "fstring", "the formatted value is substituted into the text", "reply"],
            ],
        },
    },
    {
        "id": "ClipboardProgramUses",
        "pattern": "SetOfUses",
        "title": "What the chapter's clipboard programs let a user do",
        "concepts": ["BulletPointAdder", "AlternatingText", "InputValidation", "PigLatin", "TablePrinter", "ClipboardModule"],
        "also_from": ["ProjectPrograms", "ClipboardAndPrograms", "ClipboardPrograms"],
        "read_from": "chapter 8, the clipboard and programs section: the user copies text, the bullet point adder stars every line, the alternating text program switches case by position, the validation functions reject badly formed input, the Pig Latin program translates a message, and the table printer prints a table of strings",
        "why": "the passage lists what the user and the clipboard programs each do with text on the clipboard - add bullets, alternate case, validate input, translate to Pig Latin, print a table - a set of uses by actors, not a sequence",
        "data": {
            "system": "THE CHAPTER'S CLIPBOARD PROGRAMS",
            "actors": [{"id": "user", "label": "User"}, {"id": "program", "label": "Clipboard program"}],
            "usecases": [
                {"id": "copy", "label": "Copy text onto the clipboard before running a program"},
                {"id": "bullet", "label": "Add a star and a space to the front of every line"},
                {"id": "alternate", "label": "Switch lower and upper case by position in the text"},
                {"id": "validate", "label": "Reject input that is not decimal or not alphanumeric"},
                {"id": "pig", "label": "Translate the typed message into Pig Latin"},
                {"id": "table", "label": "Print a table of strings with padded, right-justified columns"},
                {"id": "paste", "label": "Read the finished text back off the clipboard"},
            ],
            "links": [["user", "copy"], ["user", "validate"], ["user", "pig"], ["user", "paste"], ["program", "bullet"], ["program", "alternate"], ["program", "table"]],
        },
    },
    {
        "id": "StringMethodsAtAGlance",
        "pattern": "TopicAndParts",
        "title": "String methods at a glance: five jobs, one rule",
        "concepts": ["StringMethods", "TextCase", "TextChecks", "JoiningAndSplittingText", "TextSpacing", "Searching"],
        "also_from": ["ChangingCase", "CaseTests", "CaseFolding", "CharacterTests", "StartsEndsWith", "UnicodeDigits",
                      "JoinMethod", "SplitMethod", "JustifyMethods", "StripMethods", "PrefixSuffixRemoval", "FindAndCount", "ReplaceMethod"],
        "read_from": "chapter 8, the opening of the string methods branch and its five subsections: a method returns a new value and never changes the string it is called on, and the subsections group the methods by case, by character checks, by joining and splitting, by spacing and by searching",
        "why": "the section classifies one topic, string methods, by the job each group does, and lists examples under each - a topic and its parts, laid out to remember, with the one rule that holds for every part stated once at the root",
        "data": {
            "root": "String methods return a new string",
            "branches": [
                {"label": "Text case: converting and testing letters", "children": ["upper() and lower() return a new string", "isupper() and islower() test the string as it stands", "casefold() is a stronger relative of lower()"]},
                {"label": "Text checks: what characters a string holds", "children": ["isalpha(), isalnum(), isdecimal() and isspace()", "startswith() and endswith() test only one end", "the Unicode character database decides the answer"]},
                {"label": "Joining and splitting text", "children": ["join() returns one string from a list", "split(sep) cuts at every occurrence of a separator", "split() with no argument cuts at whitespace"]},
                {"label": "Text spacing: padding and trimming", "children": ["rjust(), ljust() and center() pad a string", "strip() removes characters from the ends", "removeprefix() and removesuffix() remove exact text"]},
                {"label": "Searching: finding and replacing", "children": ["find() returns the index of the first occurrence", "count() counts non-overlapping occurrences", "replace() returns a new string with text swapped out"]},
            ],
        },
    },
    {
        "id": "ChoosingASplit",
        "pattern": "Workflow",
        "title": "Choosing which method cuts a string into pieces",
        "concepts": ["SplitMethod", "WhitespaceSplit", "SplitLines", "PartitionMethod"],
        "also_from": ["JoiningAndSplittingText", "StringMethods"],
        "read_from": "chapter 8, the joining and splitting text section: split(sep) cuts at every occurrence of a separator, split() with no argument cuts at whitespace, splitlines() cuts at line boundaries, and partition(sep) cuts at only the first occurrence and keeps the separator",
        "why": "the explanations describe what the programmer decides in order when a string must be cut into pieces - is the goal line boundaries, is the separator whitespace, should the separator itself be kept - with a different method chosen on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "A string is cut at every occurrence of a separator"},
                {"id": "lines", "label": "Is a line boundary the separator?", "kind": "decision"},
                {"id": "splitlines", "label": "splitlines(): recognising every line boundary"},
                {"id": "sep", "label": "Keep the separator itself, or is it discarded?", "kind": "decision"},
                {"id": "partition", "label": "partition(sep) keeps the separator itself"},
                {"id": "whitespace", "label": "Is the separator a run of whitespace, not one character?", "kind": "decision"},
                {"id": "splitnoarg", "label": "split() with no argument cuts at runs of whitespace"},
                {"id": "splitsep", "label": "split(sep) cuts the string at every occurrence"},
            ],
            "flows": [["start", "need"], ["need", "lines"], ["lines", "splitlines", "yes"], ["lines", "sep", "no"], ["sep", "partition", "yes"], ["sep", "whitespace", "no"], ["whitespace", "splitnoarg", "yes"], ["whitespace", "splitsep", "no"], ["splitlines", "end"], ["partition", "end"], ["splitnoarg", "end"], ["splitsep", "end"]],
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
    f = sorted(glob.glob(os.path.join(here, "ch08-page", "page_data_v*.json")))
    if not f:
        print("no page_data yet; run sen0414_page_data first"); sys.exit(2)
    nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-24s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
