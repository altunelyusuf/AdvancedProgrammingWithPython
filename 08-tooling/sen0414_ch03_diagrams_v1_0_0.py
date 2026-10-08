#!/usr/bin/env python3
"""SEN0414, chapter 3 (Loops and modules, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of modules and imports a use-case diagram, the life of a loop or an iterator a state
diagram, an exchange between a program, its modules and the player a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module
of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0) so that it is reused by every course.

This module is the corpus layer for the chapter's diagrams: each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as (the diagram type follows from the mapping, never from the
author), the passage it was read from (also_from names further concepts whose explanations the content draws on, without the
diagram being shown under them), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects (see the mapping's cme:elements). Nothing here says more than the
chapter's own explanations: every element label is made of words that occur in the explanations of the accompanying
concepts or their section, and run_checks() measures that (the grounding ratio) besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "LoopExecution",
        "pattern": "Workflow",
        "title": "How a loop runs its block, with break and continue",
        "concepts": ["WhileStatement", "ForStatement", "BreakStatement", "ContinueStatement"],
        "also_from": ["Loop", "Iteration", "LoopElseClause", "LoopEnding", "IteratorObject"],
        "read_from": "chapter 3, the While statement, For statement, Break statement and Continue statement sections: While statement (repeats its block as long as its condition is true, tested at the start of each iteration), For statement (takes each item of an iterable in turn and assigns it to its variable), Break statement (ends the loop immediately, skipping the else clause), Continue statement (jumps back to the start of the loop and reevaluates the condition, or takes the next item), Loop else clause (runs when the loop finishes without executing break)",
        "why": "the explanations describe what Python does with a loop in order - test the condition or take the next item, execute the block, jump back, leave on break, skip on continue, run the else clause at the end - a workflow with decisions",
        "data": {
            "nodes": [
                {"id": "kind", "label": "Is it a while loop or a for loop?", "kind": "decision"},
                {"id": "cond", "label": "Is the condition true at the start of this iteration?", "kind": "decision"},
                {"id": "items", "label": "Does the iterator have a next item?", "kind": "decision"},
                {"id": "assign", "label": "Assign the item to the loop variable"},
                {"id": "block", "label": "Execute the indented block, one iteration"},
                {"id": "brk", "label": "Does execution reach a break statement?", "kind": "decision"},
                {"id": "cont", "label": "Does execution reach a continue statement?", "kind": "decision"},
                {"id": "skip", "label": "Skip the rest of the block and jump back to the start of the loop"},
                {"id": "back", "label": "At the end of the block, execution jumps back to the start"},
                {"id": "leave", "label": "Leave the loop immediately and skip the else clause"},
                {"id": "els", "label": "The loop finishes without break: the else clause runs"},
            ],
            "flows": [["start", "kind"], ["kind", "cond", "while"], ["kind", "items", "for"], ["cond", "block", "yes"], ["cond", "els", "no"], ["items", "assign", "yes"], ["items", "els", "no"], ["assign", "block"], ["block", "brk"], ["brk", "leave", "yes"], ["brk", "cont", "no"], ["cont", "skip", "yes"], ["cont", "back", "no"], ["skip", "kind"], ["back", "kind"], ["leave", "end"], ["els", "end"]],
        },
    },
    {
        "id": "ModuleUses",
        "pattern": "SetOfUses",
        "title": "Who uses modules and imports, and for what",
        "concepts": ["Module", "ImportStatement", "StandardLibrary", "ModuleSearchPath"],
        "also_from": ["ImportForm", "MultipleImport", "StarImport", "FromImport", "ModuleFile", "ModuleNamespace", "RandomModule", "SysModule", "ModuleNameClash"],
        "read_from": "chapter 3, the Module branch: Module (a program containing a related group of functions that can be embedded in your programs), Import statement (the import keyword, the name of the module and optionally more names separated by commas), Star import (from random import *, calls no longer need the random. prefix), From import (from math import sqrt), Standard library (the set of modules that Python comes with; built-in functions need no import), Module search path (the interpreter searches for a built-in module, then for a file named spam.py in the directories given by sys.path)",
        "why": "the branch lists what a program and the interpreter do with modules - import one or several, bring names in without the prefix, call functions through dotted names, search the path, load the file - a set of uses by actors, not a sequence",
        "data": {
            "system": "MODULES AND IMPORTS",
            "actors": [{"id": "program", "label": "Program"}, {"id": "interpreter", "label": "Python interpreter"}],
            "usecases": [
                {"id": "one", "label": "Import one module of the standard library, such as import random"},
                {"id": "several", "label": "Import several modules separated by commas: import random, sys"},
                {"id": "star", "label": "Bring all the public names in with from random import *"},
                {"id": "chosen", "label": "Import chosen names directly, as in from math import sqrt"},
                {"id": "dotted", "label": "Call a function through a dotted name, such as random.randint()"},
                {"id": "builtin", "label": "Call a built-in function such as print() without any import"},
                {"id": "search", "label": "Search for a built-in module, then for a file in sys.path"},
                {"id": "load", "label": "Load the module file and create its own namespace"},
            ],
            "links": [["program", "one"], ["program", "several"], ["program", "star"], ["program", "chosen"], ["program", "dotted"], ["program", "builtin"], ["interpreter", "search"], ["interpreter", "load"]],
        },
    },
    {
        "id": "LoopLife",
        "pattern": "LifeCycle",
        "title": "The life of a loop: entered, iterating, ended",
        "concepts": ["LoopCompletion", "LoopElseClause", "LoopEnding", "LoopVariableScope"],
        "also_from": ["Loop", "Iteration", "WhileStatement", "ForStatement", "BreakStatement", "ExitFunction", "IteratorObject"],
        "read_from": "chapter 3, the Loop completion section: Loop completion (whether the loop ended by exhausting its supply or by a break), Loop else clause (runs when the loop finishes without executing break), Endings of a loop (the condition becomes false or the iterator is exhausted, both run the else clause; a break, a return or an unhandled exception such as the SystemExit raised by sys.exit() leaves it, none run the else clause)",
        "why": "the explanations describe states a loop is in - not yet entered, executing its block, ended one way or another - and the events that move it between them: a life cycle",
        "data": {
            "states": [
                {"id": "before", "label": "Before the loop: the loop variable has no value yet"},
                {"id": "iterating", "label": "Iterating: the block is executed, one iteration after another"},
                {"id": "elseclause", "label": "Finished without break: the else clause is executed"},
                {"id": "broken", "label": "Ended by break: the else clause is skipped"},
                {"id": "left", "label": "Left by return, SystemExit or an unhandled exception"},
            ],
            "initial": "before",
            "final": ["elseclause", "broken", "left"],
            "transitions": [["before", "iterating", "execution reaches the while or for statement"], ["iterating", "iterating", "the condition is still true, or the iterator has a next item"], ["iterating", "elseclause", "the condition becomes false, or the iterator is exhausted"], ["iterating", "broken", "a break statement ends the loop immediately"], ["iterating", "left", "a return statement, sys.exit() or an exception not handled inside"]],
        },
    },
    {
        "id": "GuessTheNumberInteraction",
        "pattern": "Interaction",
        "title": "Guess the Number: the program, the random module and the player",
        "concepts": ["GuessTheNumber", "RandomModule", "ImportStatement"],
        "also_from": ["ForStatement", "BreakStatement", "RangeStartStop", "StandardModule", "ModuleNamespace", "LoopElseClause"],
        "read_from": "chapter 3, the Guess the number section: Guess the Number (the computer picks a secret number between 1 and 20 and the player has six chances to find it, receiving the hint too low or too high after each wrong guess; an import statement, a call to random.randint(), a for loop over range(1, 7), conversions with int() and str(), an if, elif and else chain, and a break), Random module (random.randint(a, b) returns a random integer N such that a <= N <= b)",
        "why": "the program is an exchange of messages between parties - the program, the random module it imports and the player - in an order that matters: an interaction",
        "data": {
            "participants": [{"id": "program", "label": "Guess the Number program"}, {"id": "random", "label": "random module"}, {"id": "player", "label": "Player"}],
            "messages": [
                ["program", "random", "import random, then call random.randint(1, 20)"],
                ["random", "program", "a random integer between 1 and 20: the secret number", "reply"],
                ["program", "player", "I am thinking of a number between 1 and 20"],
                ["program", "program", "for loop over range(1, 7): six chances"],
                ["program", "player", "Take a guess"],
                ["player", "program", "a guess, typed as text and converted with int()", "reply"],
                ["program", "player", "the hint too low or too high after each wrong guess"],
                ["program", "program", "the guess is the secret number: break ends the loop"],
                ["program", "player", "Good job! You guessed my number in a number of guesses, with str()"],
            ],
        },
    },
    {
        "id": "RangeMap",
        "pattern": "TopicAndParts",
        "title": "The range: forms of the call and properties of the result",
        "concepts": ["RangeSequence", "RangeStop", "RangeStartStop", "RangeStep", "RangeDescending", "LazyRange", "HalfOpenRange", "RangeOperations"],
        "also_from": ["ForStatement"],
        "read_from": "chapter 3, the Range sequence group: Range stop (range(10) generates 10 values, the end point is never part of the sequence), Range start stop (range(12, 16) prints 12, 13, 14 and 15), Range step (range(0, 10, 2) counts from 0 to 8 in intervals of two), Range descending (range(5, -1, -1) counts down from five to zero), Lazy range (produces its values when iterated, without really making the list), Half-open range (the start is included and the end is excluded), Range operations (length, membership, indexing, slicing; not concatenation or repetition)",
        "why": "the group classifies one topic, the range, by the forms of the call and by the properties of the result, and lists the examples under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "The range: an immutable sequence of integers",
            "branches": [
                {"label": "Forms of the call", "children": ["range(stop): range(5) gives 0, 1, 2, 3, 4", "range(start, stop): range(12, 16) gives 12, 13, 14, 15", "range(start, stop, step): range(0, 10, 2) gives 0, 2, 4, 6, 8", "A negative step counts down: range(5, -1, -1)"]},
                {"label": "Half-open: the start is included, the end is excluded", "children": ["The end point is never part of the generated sequence", "range(10) generates the legal indices of a sequence of length 10", "Fewer bugs: neighbouring ranges join without a gap"]},
                {"label": "Lazy: an object, not a list", "children": ["Printing range(10) displays range(0, 10)", "Returns the successive items when you iterate over it", "Saves space: it does not store its values"]},
                {"label": "Operations of a sequence", "children": ["Length, membership tests with in, indexing and slicing", "Index lookup", "Not concatenation or repetition"]},
            ],
        },
    },
    {
        "id": "IteratorLife",
        "pattern": "LifeCycle",
        "title": "The life of an iterator inside a for loop",
        "concepts": ["IterationProtocol", "IterableObject", "IteratorObject"],
        "also_from": ["ForStatement", "LoopEnding", "LazyRange"],
        "read_from": "chapter 3, the Iteration protocol section: Iteration protocol (the loop asks the iterable for an iterator; the iterator hands out the items one at a time and announces when there are no more), Iterable (an object capable of returning its members one at a time, such as list, str, tuple, dict and range), Iterator (repeated calls to __next__() or next() return successive items of the stream; when no more data are available a StopIteration exception is raised and the iterator is exhausted)",
        "why": "the explanations describe states the object walked through is in - an iterable not yet asked, an iterator handing out items, an exhausted iterator - and the calls that move it between them: a life cycle",
        "data": {
            "states": [
                {"id": "iterable", "label": "Iterable: an object capable of returning its members one at a time"},
                {"id": "iterator", "label": "Iterator: a stream of data, returning successive items"},
                {"id": "exhausted", "label": "Exhausted: no more data are available"},
            ],
            "initial": "iterable",
            "final": ["exhausted"],
            "transitions": [["iterable", "iterator", "the for loop asks the iterable for an iterator"], ["iterator", "iterator", "next() returns the next item; the loop runs its block once"], ["iterator", "exhausted", "a StopIteration exception is raised instead of an item"], ["exhausted", "exhausted", "the loop ends; the else clause runs if there is one"]],
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
    ch = re.search(r"_(ch\d+)_diagrams", os.path.basename(__file__)).group(1)
    f = sorted(glob.glob(os.path.join(here, ch + "-page", "page_data_v*.json")), key=lambda p: [int(x) for x in p.rsplit("_v", 1)[1][:-5].split("_")])
    if f: nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
