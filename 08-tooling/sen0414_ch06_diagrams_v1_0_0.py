#!/usr/bin/env python3
"""SEN0414, chapter 6 (Lists, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

Same contract as sen0414_ch05_diagrams_v1_0_0.py: the owner's ruling of 2026-10-07 - a paragraph gets the diagram its narrative calls for,
and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl), so each entry here declares its PATTERN and the type follows from the mapping, never from the author.
Each entry names the concepts whose paragraphs it accompanies (also_from: further concepts whose explanations the content draws on), the
passage it was read from, one sentence on why the pattern fits, and the content in the element names the renderer of that type expects.
Every element label is made of words that occur in the explanations of the accompanying concepts or their branch, and run_checks()
measures that (the grounding ratio) besides the structural rules. This chapter raises the bar from 0.8 to 0.85 (the brief's figure).

Nine diagrams: three workflows (searching a list, removing items, choosing how to loop), two life cycles (a list's contents, a name's
view of a list), two interactions (a function receiving a list, copying a nested list), one set of uses and one mind map of the
operations that change a list.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "FindingAValue",
        "pattern": "Workflow",
        "title": "How a program asks whether a value is in a list and where",
        "concepts": ["Membership", "IndexMethod", "ShortCircuit"],
        "also_from": ["Searching", "Index", "ListLength", "SearchingOrdering"],
        "read_from": "chapter 6, the Searching a list group: in and not in (an expression that evaluates to True or False), index (returns the position of the first match, raises a ValueError when the value is absent), and short-circuiting (a test on the left of and guards an expression on the right)",
        "why": "the explanations describe what the programmer does in order - ask whether the value is in the list, ask for its position only when it is there, guard the item with a test of the length when the list may be empty - with choices on the way: a workflow",
        "data": {
            "nodes": [
                {"id": "ask", "label": "Is the value in the list? Test it with the in operator", "kind": "decision"},
                {"id": "report", "label": "The expression evaluates to False: the value is not in the list"},
                {"id": "where", "label": "Is the position of the value needed?", "kind": "decision"},
                {"id": "index", "label": "Call the index method: it returns the index of the first match"},
                {"id": "first", "label": "Does the program read the first item of a list that may be empty?", "kind": "decision"},
                {"id": "guard", "label": "Write len(spam) > 0 and spam[0] == 'cat': short-circuiting protects"},
                {"id": "plain", "label": "Use the value, which is True for the in operator"},
            ],
            "flows": [["start", "ask"], ["ask", "report", "no"], ["ask", "where", "yes"], ["report", "end"], ["where", "index", "yes"], ["where", "first", "no"], ["index", "first"], ["first", "guard", "yes"], ["first", "plain", "no"], ["guard", "end"], ["plain", "end"]],
        },
    },
    {
        "id": "RemovingItems",
        "pattern": "Workflow",
        "title": "Choosing how to remove an item from a list",
        "concepts": ["DelStatement", "RemoveMethod", "PopMethod"],
        "also_from": ["Removing", "ChangingLists", "IndexMethod", "Index"],
        "read_from": "chapter 6, the Removing items group: del (when you know the index of the value you want to remove), remove (when you know the value itself; the first match only; a ValueError when it is absent), pop (removes the item at an index, by default the last, and returns it; an IndexError on an empty list)",
        "why": "the passage is a choice made step by step from what the programmer knows - the index or the value - and whether the removed item is needed afterwards, which is a workflow with decisions",
        "data": {
            "nodes": [
                {"id": "know", "label": "Does the programmer know the index of the value to remove?", "kind": "decision"},
                {"id": "needed", "label": "Is the removed item needed afterwards?", "kind": "decision"},
                {"id": "pop", "label": "Call the pop method: it removes the item and returns it"},
                {"id": "del", "label": "Use the del statement: it removes the item at the index"},
                {"id": "value", "label": "Call the remove method with the value itself"},
                {"id": "first", "label": "The first match is removed; later matches stay in the list"},
                {"id": "absent", "label": "Is the value missing from the list?", "kind": "decision"},
                {"id": "error", "label": "Python raises a ValueError: the value is not in the list"},
            ],
            "flows": [["start", "know"], ["know", "needed", "yes"], ["know", "value", "no: only the value"], ["needed", "pop", "yes"], ["needed", "del", "no"], ["pop", "end"], ["del", "end"], ["value", "absent"], ["absent", "error", "yes"], ["absent", "first", "no"], ["error", "end"], ["first", "end"]],
        },
    },
    {
        "id": "ChoosingALoop",
        "pattern": "Workflow",
        "title": "Choosing the form of a loop over a list",
        "concepts": ["RangeLenLoop", "EnumerateLoop", "MutationWhileIterating", "ListComprehension"],
        "also_from": ["Looping", "LoopsUnpacking", "MultipleAssignment"],
        "read_from": "chapter 6 and the Python documentation, the Looping over a list group: a for loop over the items, range(len(...)) for the indexes, enumerate for the index and the item, a list comprehension for a new list, and the warning not to change a list while a loop is walking through it",
        "why": "the group compares forms by what the loop body needs - the item, the index, both, or a new list - and warns about one case, which is a choice walked through question by question: a workflow",
        "data": {
            "nodes": [
                {"id": "build", "label": "Does the loop build a new list from the old one?", "kind": "decision"},
                {"id": "comp", "label": "Write a list comprehension: an expression, a for clause and an if clause"},
                {"id": "remove", "label": "Does the loop remove or add items of the list it is reading?", "kind": "decision"},
                {"id": "copy", "label": "Loop over a copy or build a new list instead of changing the old one"},
                {"id": "idx", "label": "Does the loop body need the index of each item?", "kind": "decision"},
                {"id": "enum", "label": "Use enumerate: it returns the index and the item on each iteration"},
                {"id": "plain", "label": "Loop over the list itself: the loop variable is each item in turn"},
                {"id": "place", "label": "Must the loop change items in place by index?", "kind": "decision"},
                {"id": "rng", "label": "Use range(len(some_list)) to iterate over the indexes"},
            ],
            "flows": [["start", "build"], ["build", "comp", "yes"], ["build", "remove", "no"], ["comp", "end"], ["remove", "copy", "yes"], ["remove", "idx", "no"], ["copy", "end"], ["idx", "place", "yes"], ["idx", "plain", "no"], ["place", "rng", "yes"], ["place", "enum", "no: only to read"], ["enum", "end"], ["plain", "end"], ["rng", "end"]],
        },
    },
    {
        "id": "ListContents",
        "pattern": "LifeCycle",
        "title": "The life of a list: from empty to filled and back",
        "concepts": ["List", "AppendMethod", "InsertMethod", "ExtendMethod", "PopMethod"],
        "also_from": ["ListLength", "Adding", "Removing", "DelStatement", "RemoveMethod", "ChangingLists"],
        "read_from": "chapter 6, the List and Changing a list sections: the empty list [] contains no values; append, insert and extend add items; del, remove and pop take items away; the length of a list changes as items are added or removed",
        "why": "the explanations describe the states a list is in - empty, with items - and the events that move it from one to the next, append and its relatives forward and pop and its relatives back: a life cycle",
        "data": {
            "states": [
                {"id": "empty", "label": "Empty: the list [] contains no values and its length is 0"},
                {"id": "filled", "label": "Filled: the list holds items in order and has a length"},
                {"id": "changed", "label": "Changed in place: items replaced, added or removed"},
            ],
            "initial": "empty",
            "final": [],
            "transitions": [["empty", "filled", "append, insert or extend adds items"], ["filled", "filled", "append, insert or extend adds more items"], ["filled", "changed", "an item is replaced by assignment to an index"], ["changed", "filled", "the list is still one list, now with other items"], ["filled", "empty", "del, remove or pop takes the last item away"]],
        },
    },
    {
        "id": "NameAndList",
        "pattern": "LifeCycle",
        "title": "A list and its names: shared, then copied",
        "concepts": ["Aliasing", "ShallowCopy", "DeepCopy"],
        "also_from": ["References", "Copying", "ListArguments", "ReplicationAliasing", "SequencesReferences", "MutableImmutable"],
        "read_from": "chapter 6, the References and Copying groups: a variable holds a reference; the assignment copies only the reference, so two names refer to one list; copy.copy makes a separate list that shares the inner lists; copy.deepcopy copies the inner lists as well",
        "why": "the passage follows one list through the states it is in as the program assigns, copies and changes it - one name, shared by two names, copied shallowly, copied deeply - and the events that move it on: a life cycle",
        "data": {
            "states": [
                {"id": "one", "label": "One name: a variable refers to the list"},
                {"id": "shared", "label": "Shared: two names refer to the same list"},
                {"id": "shallow", "label": "Shallow copy: a separate list that shares the inner lists"},
                {"id": "deep", "label": "Deep copy: separate lists, nothing shared with the original"},
            ],
            "initial": "one",
            "final": [],
            "transitions": [["one", "shared", "eggs = spam copies only the reference"], ["shared", "shared", "a change made through either name shows through both"], ["one", "shallow", "copy.copy makes a duplicate of the list"], ["shallow", "shallow", "a change to an inner list shows through both"], ["one", "deep", "copy.deepcopy copies the inner lists as well"]],
        },
    },
    {
        "id": "ListArgument",
        "pattern": "Interaction",
        "title": "What happens when a function receives a list",
        "concepts": ["ListArguments", "Aliasing"],
        "also_from": ["References", "AppendMethod", "MutableImmutable", "SequencesReferences"],
        "read_from": "chapter 6, the Arguments passage of the References section: when a function is called, Python copies the reference of the argument to the parameter variable, so for a list the code in the function modifies the original value in place",
        "why": "the passage is an exchange between the calling code, the function and the list in an order that matters - the call, the copy of the reference, the append, the return, the print - which is an interaction",
        "data": {
            "participants": [{"id": "caller", "label": "Calling code"}, {"id": "function", "label": "Function eggs"}, {"id": "list", "label": "The list value"}],
            "messages": [
                ["caller", "list", "spam = [1, 2, 3]: the variable refers to the list"],
                ["caller", "function", "eggs(spam): Python copies the reference to the parameter"],
                ["function", "list", "some_parameter.append('Hello') modifies the list in place"],
                ["function", "caller", "returns: the function gives no new value back", "reply"],
                ["caller", "list", "print(spam) reads the same list"],
                ["list", "caller", "[1, 2, 3, 'Hello']: the change survives the call", "reply"],
            ],
        },
    },
    {
        "id": "NestedCopy",
        "pattern": "Interaction",
        "title": "Copying a list that contains lists: what is shared",
        "concepts": ["ShallowCopy", "DeepCopy", "ReplicationAliasing"],
        "also_from": ["Copying", "Aliasing", "NestedList", "References"],
        "read_from": "chapter 6 and the copy module documentation: a shallow copy constructs a new compound object and inserts references to the objects found in the original; a deep copy inserts copies; repeating a list of lists repeats references to one inner list",
        "why": "the passage is an exchange between the program, the copy module and the lists in an order that matters - the program asks for a copy, changes the copy, and looks at the original - and the answer differs between the two functions: an interaction",
        "data": {
            "participants": [{"id": "program", "label": "Program"}, {"id": "copymod", "label": "Module copy"}, {"id": "original", "label": "Original list"}, {"id": "duplicate", "label": "Duplicate list"}],
            "messages": [
                ["program", "copymod", "copy.copy(spam): ask for a shallow copy"],
                ["copymod", "duplicate", "a new list that holds references to the same inner lists"],
                ["program", "duplicate", "cheese[0].append(9): change an inner list"],
                ["original", "program", "the original shows the change too: the inner list is shared", "reply"],
                ["program", "copymod", "copy.deepcopy(spam): ask for a deep copy"],
                ["copymod", "duplicate", "copies of the inner lists as well, nothing shared"],
                ["original", "program", "a change to the duplicate no longer reaches the original", "reply"],
            ],
        },
    },
    {
        "id": "ListUses",
        "pattern": "SetOfUses",
        "title": "Who uses a list, and for what",
        "concepts": ["List", "Index", "Slice", "Membership", "SortMethod"],
        "also_from": ["ListModel", "ListValues", "ItemAssignment", "AppendMethod", "RemoveMethod", "IndexMethod", "EnumerateLoop", "MultipleAssignment", "MagicEightBall", "RandomChoice"],
        "read_from": "chapter 6, the list data type and the searching and ordering branches: the programmer reads items by index, takes slices, replaces, adds, removes, searches and sorts; the interpreter raises errors for a bad index or a missing value; the user types the names the program checks and asks the Magic 8 Ball",
        "why": "the passage lists what the programmer, the user and the interpreter do with a list - read, slice, change, search, sort, check, answer - which is a set of uses by actors, not a sequence",
        "data": {
            "system": "A LIST IN A PROGRAM",
            "actors": [{"id": "programmer", "label": "Programmer"}, {"id": "user", "label": "User"}, {"id": "interpreter", "label": "Python interpreter"}],
            "usecases": [
                {"id": "read", "label": "Select an item with an index in square brackets"},
                {"id": "slice", "label": "Take several items at once as a new list with a slice"},
                {"id": "replace", "label": "Replace an item by assigning to its index"},
                {"id": "add", "label": "Add items with the append and insert methods"},
                {"id": "remove", "label": "Remove items with del, remove or pop"},
                {"id": "search", "label": "Search the list with the in operator and the index method"},
                {"id": "sort", "label": "Put the items in order with the sort method"},
                {"id": "unpack", "label": "Assign the items to several variables in one line"},
                {"id": "typename", "label": "Type a pet name that the program looks for in the list"},
                {"id": "ask", "label": "Ask a question and read a random answer from the list"},
                {"id": "indexerr", "label": "Raise an IndexError when an index is outside the list"},
                {"id": "valueerr", "label": "Raise a ValueError when the value is not in the list"},
            ],
            "links": [["programmer", "read"], ["programmer", "slice"], ["programmer", "replace"], ["programmer", "add"], ["programmer", "remove"], ["programmer", "search"], ["programmer", "sort"], ["programmer", "unpack"], ["user", "typename"], ["user", "ask"], ["interpreter", "indexerr"], ["interpreter", "valueerr"]],
        },
    },
    {
        "id": "ChangesInPlace",
        "pattern": "TopicAndParts",
        "title": "Changing a list in place: replace, add, remove and reorder",
        "concepts": ["ChangingLists", "ItemAssignment", "AppendMethod", "PopMethod", "SortMethod"],
        "also_from": ["Replacing", "Adding", "Removing", "Ordering", "InsertMethod", "ExtendMethod", "DelStatement", "RemoveMethod", "ReverseMethod", "RandomShuffle", "SortedFunction"],
        "read_from": "chapter 6, the Changing a list branch and the Ordering group: replacing by assignment to an index; adding with append, insert and extend; removing with del, remove and pop; reordering with sort, reverse and shuffle; the methods change the list in place and return None, while sorted returns a new list",
        "why": "the branches classify one topic, the ways a list can be changed, by what the operation does to the list and list the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "Changing a list in place: the methods return None",
            "branches": [
                {"label": "Replace an item", "children": ["Assign to an index: spam[1] = 'aardvark'", "A negative index replaces from the end"]},
                {"label": "Add items", "children": ["append adds one item at the end", "insert puts an item before a given index", "extend adds every item of another list"]},
                {"label": "Remove items", "children": ["del removes the item at an index", "remove removes the first item equal to a value", "pop removes an item and returns it"]},
                {"label": "Reorder the items", "children": ["sort puts the items in order", "reverse turns the order around", "random.shuffle puts the items in random order", "sorted returns a new list instead"]},
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
    """share of a diagram's content words that occur in the explanations of its concepts (every paragraph of each, and of their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + " ".join(p["text"] for p in by[c].get("paras") or []) + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
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
            if n and h / n < 0.85: bad.append("%s: grounding %d/%d below 0.85; words not in the concepts' explanations: %s" % (d["id"], h, n, ", ".join(miss)))
    return bad


if __name__ == "__main__":
    import sys, json, glob, os, re
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import sen0414_ch06_corpus_v1_0_0 as _C
    nodes = [{"id": n[0], "label": n[1], "parent": n[3], "body": _C.facet_text(n[5]), "definition": (n[4][1] if n[4] else "")} for n in _C.NODES]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
