#!/usr/bin/env python3
"""SEN0414, chapter 9 (Text Pattern Matching with Regular Expressions, Automate the Boring Stuff with Python, 3rd
edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a
use-case diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and
its parts a mind map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the
narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry
names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was
read from (also_from names further concepts whose explanations the content draws on), one sentence saying why the
pattern fits, and the diagram's content in the element names the renderer of that type expects. Every element label
is made of words that occur in the explanations of the accompanying concepts or their section; run_checks()
measures that (the grounding ratio) besides the structural rules. This module follows the layout of
sen0414_ch08_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of
another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ChoosingACharacterRule",
        "pattern": "Workflow",
        "title": "Choosing the rule for one position in a pattern",
        "concepts": ["CharacterClass", "NegativeClass", "ShorthandClasses", "DotCharacter"],
        "also_from": ["CharacterSets", "UnicodeShorthand", "PatternSyntax"],
        "read_from": "chapter 9, the character sets section: a character class in square brackets matches one character from a set, a caret negates the class, a shorthand such as digit or word or whitespace stands for a class, and the dot matches almost any character",
        "why": "the explanations describe what a programmer decides in order when one position of a pattern is being written - is almost any character allowed, is a shorthand such as digit enough, should the set be negated, or does the position need an exact set of characters - with a different choice made on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "One position in the text may be a class or almost any character"},
                {"id": "any", "label": "Almost any character, matched by the dot, except a newline?", "kind": "decision"},
                {"id": "dot", "label": "The dot matches any character except a newline"},
                {"id": "shorthand", "label": "A shorthand class, such as digit, word or whitespace characters?", "kind": "decision"},
                {"id": "shclass", "label": "A shorthand class stands for digit, word or whitespace characters"},
                {"id": "negate", "label": "A caret after the opening bracket, negating the class?", "kind": "decision"},
                {"id": "negclass", "label": "A caret after the opening bracket negates the class"},
                {"id": "charclass", "label": "Square brackets define a class that matches one character from the set"},
            ],
            "flows": [["start", "need"], ["need", "any"], ["any", "dot", "yes"], ["any", "shorthand", "no"],
                      ["shorthand", "shclass", "yes"], ["shorthand", "negate", "no"], ["negate", "negclass", "yes"],
                      ["negate", "charclass", "no"], ["dot", "end"], ["shclass", "end"], ["negclass", "end"],
                      ["charclass", "end"]],
        },
    },
    {
        "id": "ChoosingARepetition",
        "pattern": "Workflow",
        "title": "Choosing how many times a qualifier repeats",
        "concepts": ["OptionalQuantifier", "StarQuantifier", "PlusQuantifier", "BraceQuantifier", "GreedyAndLazy"],
        "also_from": ["Repetition", "DotStar", "PatternSyntax"],
        "read_from": "chapter 9, the repetition section: a question mark makes an item optional, a star matches zero or more, a plus matches one or more, curly brackets give an exact count or a range, and a trailing question mark on any quantifier makes it lazy instead of greedy",
        "why": "the explanations describe what a programmer decides in order when a quantifier is being chosen - is the item optional, is a range of counts needed, is the match meant to be the smallest one possible rather than the largest - with a different quantifier chosen on each branch: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "need", "label": "An item in the pattern repeats, zero or more times or once or more"},
                {"id": "optional", "label": "Is the item allowed to be entirely absent, zero or one time?", "kind": "decision"},
                {"id": "question", "label": "A question mark after the item makes it optional"},
                {"id": "exact", "label": "An exact count in curly brackets, at least or at most?", "kind": "decision"},
                {"id": "brace", "label": "Curly brackets state exactly how many times the item repeats"},
                {"id": "atleastone", "label": "Must the item appear at least once?", "kind": "decision"},
                {"id": "plus", "label": "A plus matches the item one or more times; it must appear at least once"},
                {"id": "star", "label": "A star matches the item zero or more times; it may be absent"},
                {"id": "lazy", "label": "Taking as few repetitions as it can, instead of as many as it can?", "kind": "decision"},
                {"id": "addlazy", "label": "A question mark after the quantifier makes it lazy"},
                {"id": "keepgreedy", "label": "The quantifier is greedy, taking as many repetitions as it can"},
            ],
            "flows": [["start", "need"], ["need", "optional"], ["optional", "question", "yes"],
                      ["optional", "exact", "no"], ["exact", "brace", "yes"], ["exact", "atleastone", "no"],
                      ["atleastone", "plus", "yes"], ["atleastone", "star", "no"], ["brace", "lazy"],
                      ["plus", "lazy"], ["star", "lazy"], ["lazy", "addlazy", "yes"], ["lazy", "keepgreedy", "no"],
                      ["question", "end"], ["addlazy", "end"], ["keepgreedy", "end"]],
        },
    },
    {
        "id": "PatternToReplacedText",
        "pattern": "LifeCycle",
        "title": "A pattern's life from a raw string to a replaced string",
        "concepts": ["RawStrings", "CompileAndSearch", "MatchObjectAccess", "SubMethod"],
        "also_from": ["PatternObjects", "FindingPatterns", "Replacing", "PatternOperations"],
        "read_from": "chapter 9, the pattern objects and replacing sections: a pattern is written as a raw string, compile turns it into a Pattern object, search returns a Match object or none, and sub returns a new string with every match replaced",
        "why": "the explanations describe the states one piece of text passes through on its way from a pattern string to a replaced string - written raw, compiled, matched, replaced - and the operation that moves it from one state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "raw", "label": "Raw: the pattern is written as a raw string"},
                {"id": "compiled", "label": "Compiled: compile turns the pattern into a Pattern object"},
                {"id": "matched", "label": "Matched: search returns a Match object or none"},
                {"id": "replaced", "label": "Replaced: sub returns a new string with every match replaced"},
            ],
            "initial": "raw",
            "final": ["replaced"],
            "transitions": [
                ["raw", "compiled", "the raw string is passed to compile, which returns a Pattern object"],
                ["compiled", "matched", "the Pattern's search method is called on the text"],
                ["matched", "replaced", "the Pattern's sub method replaces every match with new text"],
                ["raw", "matched", "the bare function search is called directly, with no separate compile"],
                ["matched", "matched", "another search is run on the same text, for another match"],
            ],
        },
    },
    {
        "id": "FindallShape",
        "pattern": "Interaction",
        "title": "How findall decides the shape of what it returns",
        "concepts": ["FindallMethod", "FindallNoOverlap", "GroupingParentheses"],
        "also_from": ["Finding", "Grouping", "PatternOperations"],
        "read_from": "chapter 9, the finding and grouping sections: findall searches the text for every non-overlapping match, and the number of groups the pattern has decides whether a plain list of strings or a list of tuples of group text is returned",
        "why": "the passage is an exchange between parties in an order that matters - the pattern is searched against the text, every non-overlapping match is found, and the pattern's own groups decide the shape of the result handed back: an interaction",
        "data": {
            "participants": [
                {"id": "pattern", "label": "The pattern and its groups"},
                {"id": "text", "label": "The text"},
                {"id": "findall", "label": "The findall method"},
            ],
            "messages": [
                ["findall", "text", "every non-overlapping match in the text is found, in order"],
                ["text", "findall", "the shape of what comes back depends on the pattern's own groups", "reply"],
                ["findall", "pattern", "a plain list of matched strings comes back for no groups or exactly one"],
                ["pattern", "findall", "a list of tuples of the groups' text comes back for two or more groups", "reply"],
            ],
        },
    },
    {
        "id": "ContactExtractorUses",
        "pattern": "SetOfUses",
        "title": "What Project 3's contact extractor lets a user do",
        "concepts": ["ClipboardRoundTrip", "PhoneRegex", "EmailRegex", "ExtensionGroupIndex"],
        "also_from": ["ContactExtractor", "PatternPrograms"],
        "read_from": "chapter 9, the contact extractor section: the user copies text onto the clipboard, the program searches it with a phone pattern and an email pattern, reads the groups of each match, joins every match found, and copies the result back",
        "why": "the passage lists what the user and the program each do with text on the clipboard - copy text in, search with two patterns, read the groups, join the matches, copy text out - a set of uses by actors, not a sequence",
        "data": {
            "system": "PROJECT 3'S CONTACT EXTRACTOR",
            "actors": [{"id": "user", "label": "User"}, {"id": "program", "label": "Contact extractor program"}],
            "usecases": [
                {"id": "copyin", "label": "Copy a page of text onto the clipboard before running the program"},
                {"id": "phone", "label": "Search the text with the phone regex"},
                {"id": "email", "label": "Search the text with the email regex"},
                {"id": "index", "label": "Read the matched groups at the correct index for each pattern"},
                {"id": "join", "label": "Join every phone number and email address found into one block of text"},
                {"id": "copyout", "label": "Read the joined matches back off the clipboard"},
            ],
            "links": [["user", "copyin"], ["user", "copyout"], ["program", "phone"], ["program", "email"],
                      ["program", "index"], ["program", "join"]],
        },
    },
    {
        "id": "PatternSyntaxAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Pattern syntax at a glance: four questions, one rule each",
        "concepts": ["PatternSyntax", "Grouping", "CharacterSets", "Repetition", "Anchors"],
        "also_from": ["GroupingParentheses", "Alternation", "NamedGroups", "CharacterClass", "ShorthandClasses",
                       "OptionalQuantifier", "BraceQuantifier", "GreedyAndLazy", "StartEndAnchors", "WordBoundary",
                       "LookAround"],
        "read_from": "chapter 9, the opening of the pattern syntax branch and its four subsections: a pattern decides what to match, how many times, where, and what to keep, and the subsections group the syntax by grouping, by character sets, by repetition and by anchors",
        "why": "the section classifies one topic, pattern syntax, by the question each group of notation answers, and lists examples under each - a topic and its parts, laid out to remember, with the one question that holds for every part stated once at the root",
        "data": {
            "root": "A pattern decides what to match, how many times, where, and what to keep",
            "branches": [
                {"label": "Grouping: what is kept, and which alternative is tried",
                 "children": ["parentheses number a group from 1, read with group and groups",
                              "the pipe offers alternatives, tried left to right",
                              "a named group is read by name as well as by number"]},
                {"label": "Character sets: what one position may be",
                 "children": ["a character class in square brackets matches one character from a set",
                              "a caret after the opening bracket negates the class",
                              "a shorthand class such as digit, word or whitespace stands for a set"]},
                {"label": "Repetition: how many times a qualifier matches",
                 "children": ["a question mark makes the item optional, zero or one time",
                              "curly brackets give an exact count or a range",
                              "a trailing question mark makes a quantifier lazy instead of greedy"]},
                {"label": "Anchors: where in the text, or next to what",
                 "children": ["a caret and a dollar sign tie a pattern to the start and end of the text",
                              "a word boundary ties a pattern to the edge of a word",
                              "a lookahead or lookbehind checks text beside a position, unmatched"]},
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
    f = sorted(glob.glob(os.path.join(here, "ch09-page", "page_data_v*.json")))
    if not f:
        print("no page_data yet; run sen0414_page_data first"); sys.exit(2)
    nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-24s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
