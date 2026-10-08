#!/usr/bin/env python3
"""SEN0414, chapter 4 (Functions, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of functions by a programmer a use-case diagram, the life of a frame on the call stack a
state diagram, an exchange between the caller, the called function and the except clause a sequence diagram, a topic
and its parts a mind map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the
narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0) so that it is reused by every course.

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
        "id": "FunctionCallFlow",
        "pattern": "Workflow",
        "title": "What happens when a function is called",
        "concepts": ["FunctionCall", "ParameterAndArgument", "FunctionBody", "ReturnStatement", "ImplicitNone"],
        "also_from": ["DefStatement", "DefaultArgument", "CallStackOrder", "CallAsExpression", "FrameObject"],
        "read_from": "chapter 4, the Definition, Parameters and Return value sections: Function call (execution jumps to the first line in the function and begins executing the code there), Parameter and argument (the argument 'Al' is assigned to the parameter name), Function body (runs on each call to the end or to a return statement), Return statement (leaves the call with the value of its expression as the return value), Implicit None (Python adds return None to any function without a return statement)",
        "why": "the explanations describe what Python does with a call in order - remember the calling line, assign the arguments to the parameters, execute the body, choose the return value, return to the calling line - with two choices on the way, whether an argument was left out and whether a return statement is reached: a workflow",
        "data": {
            "nodes": [
                {"id": "reach", "label": "The program execution reaches a call, such as say_hello_to('Al')"},
                {"id": "remember", "label": "Python remembers which line of code called the function"},
                {"id": "every", "label": "Is an argument passed for every parameter?", "kind": "decision"},
                {"id": "assign", "label": "Each argument is assigned to its parameter"},
                {"id": "default", "label": "The default value written in the definition is used instead"},
                {"id": "jump", "label": "Execution jumps to the first line of the body and begins executing it"},
                {"id": "ret", "label": "Does the body reach a return statement with a value?", "kind": "decision"},
                {"id": "expr", "label": "The expression after return is evaluated: that is the return value"},
                {"id": "none", "label": "Python adds return None to the end of the function: it returns None"},
                {"id": "back", "label": "The call evaluates to the return value; execution returns to the line"},
                {"id": "forget", "label": "The parameters and local variables are forgotten"},
            ],
            "flows": [["start", "reach"], ["reach", "remember"], ["remember", "every"], ["every", "assign", "yes"], ["every", "default", "no"], ["assign", "jump"], ["default", "jump"], ["jump", "ret"], ["ret", "expr", "yes"], ["ret", "none", "no"], ["expr", "back"], ["none", "back"], ["back", "forget"], ["forget", "end"]],
        },
    },
    {
        "id": "NameResolutionFlow",
        "pattern": "Workflow",
        "title": "How Python decides which variable a name refers to",
        "concepts": ["NameResolution", "LocalScope", "EnclosingScope", "GlobalScope", "BuiltinScope", "NameError"],
        "also_from": ["GlobalStatement", "ScopeIdentification", "GlobalAccess", "LocalIsolation", "UnboundLocalError", "SameNameVariables"],
        "read_from": "chapter 4, the Namespaces and Scope rules sections: Name resolution (a name is resolved using the nearest enclosing scope, in the order local, enclosing, global, built-in), Scope identification (global statement, assignment in the function, use without assignment), Global statement (in this function, eggs refers to the global variable), UnboundLocalError (a local variable used before a value is bound), Built-in scope (print, len and int are found in the builtins namespace), NameError (raised when no scope contains the name)",
        "why": "the explanations describe a search in a fixed order - the local scope, the enclosing scope, the global scope, the built-in scope - with a question at each step and an error when every step fails: a workflow",
        "data": {
            "nodes": [
                {"id": "use", "label": "A name such as eggs is used in a code block inside a function"},
                {"id": "gstmt", "label": "Does a global statement in this function list the name?", "kind": "decision"},
                {"id": "global", "label": "The name refers to the global variable"},
                {"id": "assigns", "label": "Does the function assign the name a value, making it local?", "kind": "decision"},
                {"id": "bound", "label": "Has a value been bound to the local variable before this use?", "kind": "decision"},
                {"id": "local", "label": "The name refers to the local variable of this call"},
                {"id": "unbound", "label": "Python raises UnboundLocalError: the local variable has no value yet"},
                {"id": "enclosing", "label": "Is the name a variable of the enclosing function?", "kind": "decision"},
                {"id": "outer", "label": "The nested function reads the variable in the enclosing scope"},
                {"id": "isglobal", "label": "Is the name assigned outside all functions, in the global scope?", "kind": "decision"},
                {"id": "builtin", "label": "Is the name one Python provides, such as print, len or int?", "kind": "decision"},
                {"id": "builtins", "label": "The name is found in the builtins namespace, searched last"},
                {"id": "error", "label": "Python raises NameError: name 'eggs' is not defined"},
            ],
            "flows": [["start", "use"], ["use", "gstmt"], ["gstmt", "global", "yes"], ["gstmt", "assigns", "no"], ["assigns", "bound", "yes"], ["assigns", "enclosing", "no"], ["bound", "local", "yes"], ["bound", "unbound", "no"], ["enclosing", "outer", "yes"], ["enclosing", "isglobal", "no"], ["isglobal", "global", "yes"], ["isglobal", "builtin", "no"], ["builtin", "builtins", "yes"], ["builtin", "error", "no"], ["global", "end"], ["local", "end"], ["unbound", "end"], ["outer", "end"], ["builtins", "end"], ["error", "end"]],
        },
    },
    {
        "id": "FrameLife",
        "pattern": "LifeCycle",
        "title": "The life of a frame on the call stack",
        "concepts": ["FrameObject", "CallStackOrder", "CallStack"],
        "also_from": ["FunctionCall", "ReturnStatement", "Recursion", "Traceback", "ErrorInCall", "LocalScope", "StackInspection"],
        "read_from": "chapter 4, the Call stack section: Frame object (the record Python creates for a function call and places on the call stack; it stores the line number of the original call), Call stack order (Python remembers which line called the function so that execution can return there when it encounters a return statement), Recursion (each call has its own frame), Traceback (the lines of the calls the exception passed through), Local scope (destroyed when the call returns)",
        "why": "the explanations describe states a call's record is in - not yet created, placed on the stack, executing, waiting for another call, removed on return or by an exception - and the events that move it between them: a life cycle",
        "data": {
            "states": [
                {"id": "none", "label": "No frame: the function call has not started"},
                {"id": "placed", "label": "Frame created and placed on the call stack, storing the calling line"},
                {"id": "running", "label": "The code in the function is executing in this frame"},
                {"id": "waiting", "label": "Waiting: the function has called another function, whose frame is above"},
                {"id": "returned", "label": "Frame removed: execution returned to the line that called the function"},
                {"id": "unwound", "label": "Frame removed by an exception; the traceback lists its line"},
            ],
            "initial": "none",
            "final": ["returned", "unwound"],
            "transitions": [["none", "placed", "program execution reaches the function call"], ["placed", "running", "execution jumps to the first line in the function"], ["running", "waiting", "the function calls another function, or calls itself recursively"], ["waiting", "running", "the called function returns its value"], ["running", "returned", "a return statement is encountered, or the body ends"], ["running", "unwound", "an error happens and no except clause in this function handles it"], ["waiting", "unwound", "the error of the called function is not handled here"]],
        },
    },
    {
        "id": "CallAndErrorInteraction",
        "pattern": "Interaction",
        "title": "A call that returns, and a call that raises an error caught by except",
        "concepts": ["TryExcept", "ErrorInCall", "ZeroDivisionError", "Traceback"],
        "also_from": ["FunctionCall", "ReturnStatement", "CallStackOrder", "ExceptionObject", "ReturnValue", "FunctionBody"],
        "read_from": "chapter 4, the Exceptions section: Try and except (the code that could have an error is put in a try clause, and execution moves to the start of the except clause if an error happens), Error in a called function (errors that occur in function calls in a try block will also be caught), ZeroDivisionError (raised when the second argument of a division is zero), Traceback (printed when an exception is not handled)",
        "why": "the passage is an exchange of messages between parties - the code in the try clause, the function it calls and the except clause - in an order that matters, once with a return value and once with an error: an interaction",
        "data": {
            "participants": [{"id": "caller", "label": "Code in the try clause"}, {"id": "func", "label": "The called function spam"}, {"id": "handler", "label": "The except clause"}],
            "messages": [
                ["caller", "func", "call spam(2): the argument 2 is passed"],
                ["func", "func", "execute the body: return 42 / divide_by"],
                ["func", "caller", "the call evaluates to the return value 21.0", "reply"],
                ["caller", "func", "call spam(0): the second argument of the division will be zero"],
                ["func", "func", "42 / 0: Python raises ZeroDivisionError and creates an exception object"],
                ["func", "handler", "the error in the function call is caught by the try clause around it"],
                ["handler", "handler", "program execution moves to the start of the except clause"],
                ["handler", "caller", "the block under the except line runs; execution continues after try", "reply"],
                ["func", "caller", "with no try statement the program will crash: Python prints a traceback", "reply"],
            ],
        },
    },
    {
        "id": "FunctionUses",
        "pattern": "SetOfUses",
        "title": "What a programmer does with functions, and what Python does with them",
        "concepts": ["Deduplication", "BlackBoxFunction", "CallAsExpression", "TypeAnnotation", "FunctionNaming", "Comment"],
        "also_from": ["DefStatement", "FunctionObject", "FunctionCall", "ModuleFunction", "ReturnValue", "DeferredAnnotations", "ParameterAndArgument"],
        "read_from": "chapter 4, the Definition, Return value, Annotations and Style sections: Deduplication (getting rid of copied-and-pasted code; a fix in one place), Function as a black box (its inputs are the parameters and its output is the return value), Call as expression (a call wherever a value is expected), Function annotation (a note on a parameter or the result, stored but not enforced), Function naming (lowercase with underscores), Comment (a note for the human reader that Python ignores)",
        "why": "the passages list what a programmer does with functions - group repeated code, use a function as a black box, pass a call as an argument, annotate, name and comment it - and what Python does in return, which is a set of uses by actors, not a sequence",
        "data": {
            "system": "FUNCTIONS",
            "actors": [{"id": "programmer", "label": "Programmer"}, {"id": "python", "label": "Python"}],
            "usecases": [
                {"id": "group", "label": "Group code that runs more than once into one function"},
                {"id": "fix", "label": "Make a fix in one place instead of in every pasted copy"},
                {"id": "blackbox", "label": "Treat a function as a black box: parameters in, return value out"},
                {"id": "nest", "label": "Pass a call as an argument to another function call"},
                {"id": "annotate", "label": "Write a note on a parameter or on the result as an annotation"},
                {"id": "name", "label": "Name the function in lowercase, with words separated by underscores"},
                {"id": "comment", "label": "Comment the function for the human reader, after a hash character"},
                {"id": "build", "label": "Build a function object when the def statement is executed"},
                {"id": "store", "label": "Store the annotation without enforcing it"},
                {"id": "ignore", "label": "Ignore the comment: it is not interpreted"},
            ],
            "links": [["programmer", "group"], ["programmer", "fix"], ["programmer", "blackbox"], ["programmer", "nest"], ["programmer", "annotate"], ["programmer", "name"], ["programmer", "comment"], ["python", "build"], ["python", "store"], ["python", "ignore"]],
        },
    },
    {
        "id": "ParameterKindsMap",
        "pattern": "TopicAndParts",
        "title": "The kinds of parameter and how a call fills them",
        "concepts": ["Parameters", "ParameterAndArgument", "PositionalArgument", "NamedParameter", "PositionalOnlyParameter", "KeywordOnlyParameter", "DefaultArgument"],
        "also_from": ["FunctionCall", "NoneValue"],
        "read_from": "chapter 4, the Parameters section: Parameter and argument (the argument 'Al' is assigned to the parameter name), Positional argument (matched by its place in the call), Named parameter (identified by the name written before it, as in sep=','), Positional-only parameter (before a slash), Keyword-only parameter (after a star), Default argument (used when a call leaves the argument out; evaluated once when the function is defined)",
        "why": "the section classifies one topic, the parameter, by the way a call supplies its value - by position, by name, only by position, only by name, or not at all - and lists the rule under each: a topic and its parts, laid out to remember",
        "data": {
            "root": "Parameters: the way values get into a function",
            "branches": [
                {"label": "Argument and parameter", "children": ["Argument: the value passed in the call, such as 'Al'", "Parameter: the variable in the definition that receives it", "The parameter is forgotten when the function returns"]},
                {"label": "Positional argument: matched by its place in the call", "children": ["The first argument goes to the first parameter, the second to the second", "Swapping two arguments changes the result"]},
                {"label": "Named parameter: identified by its name in the call", "children": ["sep=',' and end are named parameters of print", "Also called keyword parameters or keyword arguments"]},
                {"label": "Positional-only parameter: before a slash", "children": ["Can be passed only by position, never by name", "Passing one by name raises a TypeError"]},
                {"label": "Keyword-only parameter: after a star", "children": ["Can be supplied only by keyword", "Never filled in by a positional argument"]},
                {"label": "Default argument: a value written in the definition", "children": ["Used when a call leaves the argument out", "Evaluated once, when the function is defined", "A mutable default is shared between calls; the remedy is None"]},
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
    ch = re.search(r"_(ch\d+)_diagrams", os.path.basename(__file__)).group(1)
    f = sorted(glob.glob(os.path.join(here, ch + "-page", "page_data_v*.json")), key=lambda p: [int(x) for x in p.rsplit("_v", 1)[1][:-5].split("_")])
    if f: nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
