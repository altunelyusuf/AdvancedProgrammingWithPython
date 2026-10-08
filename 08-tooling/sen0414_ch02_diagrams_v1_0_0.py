#!/usr/bin/env python3
"""SEN0414, chapter 2 (Flow control, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of truth values and comparisons a use-case diagram, the life of an error report a state
diagram, an exchange between the user, the program and the error report a sequence diagram, a topic and its parts a mind
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
        "id": "BranchChainExecution",
        "pattern": "Workflow",
        "title": "How execution runs through a chain of if, elif and else",
        "concepts": ["IfStatement", "ElifClause", "ElseClause", "BranchChain"],
        "also_from": ["Condition", "Block", "Clause", "Keyword", "FlowControlStatement", "ProgramExecution", "Indentation"],
        "read_from": "chapter 2, the Branching section: If statement (its block executes when the condition is True and is skipped when it is False), Elif clause (another condition, checked only if all of the previous conditions were False), Else clause (executed only when the condition of the if statement is False; it has no condition), Branch chain (exactly one if statement, any elif clauses after it, and else to be sure that at least one clause is executed)",
        "why": "the explanations describe what execution does in order - evaluate the if condition, run or skip the block, check the next elif condition only when the earlier ones were False, fall to else when nothing else has run - which is a procedure with decisions: a workflow",
        "data": {
            "nodes": [
                {"id": "ifcond", "label": "Execution reaches the if keyword and evaluates its condition"},
                {"id": "iftrue", "label": "Is the condition of the if statement True?", "kind": "decision"},
                {"id": "ifblock", "label": "Execute the indented block of the if clause"},
                {"id": "haselif", "label": "Does an elif clause follow?", "kind": "decision"},
                {"id": "elifcond", "label": "Evaluate the condition of the elif clause"},
                {"id": "eliftrue", "label": "Is the elif condition True?", "kind": "decision"},
                {"id": "elifblock", "label": "Execute the indented block of the elif clause"},
                {"id": "haselse", "label": "Does the chain end with an else clause?", "kind": "decision"},
                {"id": "elseblock", "label": "Execute the else clause: it has no condition"},
                {"id": "skip", "label": "Skip every block: no clause of the chain is executed"},
                {"id": "next", "label": "Execution continues with the statement after the chain"},
            ],
            "flows": [["start", "ifcond"], ["ifcond", "iftrue"], ["iftrue", "ifblock", "yes"], ["iftrue", "haselif", "no"], ["haselif", "elifcond", "yes"], ["haselif", "haselse", "no"], ["elifcond", "eliftrue"], ["eliftrue", "elifblock", "yes"], ["eliftrue", "haselif", "no: check the next clause"], ["haselse", "elseblock", "yes"], ["haselse", "skip", "no"], ["ifblock", "next"], ["elifblock", "next"], ["elseblock", "next"], ["skip", "next"], ["next", "end"]],
        },
    },
    {
        "id": "MatchStatementExecution",
        "pattern": "Workflow",
        "title": "How a match statement chooses a case block",
        "concepts": ["MatchStatement", "CasePattern", "Guard", "WildcardPattern"],
        "also_from": ["PatternMatching", "SequencePattern", "SoftKeyword", "Condition", "Block"],
        "read_from": "chapter 2, the Pattern matching section: Match statement (takes an expression and compares its value with successive patterns given as case blocks; only the first pattern that matches is executed; if no case matches, none of the branches runs), Case pattern (matched against the subject value; the outcome is a success or a failure and possibly the binding of matched values to names), Guard (if followed by an expression; it must succeed for the code inside the case block to execute), Wildcard pattern (the underscore always succeeds and binds no name)",
        "why": "the explanations describe a procedure in order - evaluate the subject, try each case pattern in turn, check its guard, run the first case block whose pattern and guard succeed, or run nothing - with decisions at every case: a workflow",
        "data": {
            "nodes": [
                {"id": "subject", "label": "Evaluate the expression after match: the subject value"},
                {"id": "nextcase", "label": "Take the next case block and its pattern"},
                {"id": "matches", "label": "Does the pattern match the subject value?", "kind": "decision"},
                {"id": "bind", "label": "Success: bind the matched values to names"},
                {"id": "hasguard", "label": "Is a guard, if followed by an expression, attached to the case?", "kind": "decision"},
                {"id": "guardok", "label": "Does the guard succeed?", "kind": "decision"},
                {"id": "run", "label": "Execute the code inside the case block; later cases are not tried"},
                {"id": "more", "label": "Is there another case?", "kind": "decision"},
                {"id": "none", "label": "No case matches: none of the branches runs"},
            ],
            "flows": [["start", "subject"], ["subject", "nextcase"], ["nextcase", "matches"], ["matches", "bind", "yes"], ["matches", "more", "no: failure"], ["bind", "hasguard"], ["hasguard", "guardok", "yes"], ["hasguard", "run", "no"], ["guardok", "run", "yes"], ["guardok", "more", "no"], ["more", "nextcase", "yes"], ["more", "none", "no"], ["run", "end"], ["none", "end"]],
        },
    },
    {
        "id": "ErrorReportLife",
        "pattern": "LifeCycle",
        "title": "The life of a program run that ends in an error report",
        "concepts": ["Exception", "Traceback", "SyntaxErrorKind", "ErrorKind"],
        "also_from": ["ProgramExecution", "NameErrorKind", "TypeErrorKind", "ZeroDivisionErrorKind", "FlowControlStatement"],
        "read_from": "chapter 2, the Kind of error section: Kind of error (syntax errors, which the parser finds when it reads the text, against exceptions, detected during execution in a statement that is syntactically correct), SyntaxError (raised when the parser encounters text that does not follow the grammar), Exception (an error detected while a program runs; most are not handled and result in an error report), Traceback (the report Python prints when an error stops a program: the lines through which the program reached the error, and last the kind and the message)",
        "why": "the explanations describe states a program run passes through - being read by the parser, being executed, stopped by an error, reported - and the events that move it between them, with two different entries into the error states: a life cycle",
        "data": {
            "states": [
                {"id": "parsing", "label": "The parser reads the text of the program"},
                {"id": "syntaxerror", "label": "SyntaxError: the text does not follow the grammar"},
                {"id": "executing", "label": "Execution runs the statements, one at a time"},
                {"id": "exception", "label": "An exception is detected during execution"},
                {"id": "handled", "label": "The program handles the exception and continues"},
                {"id": "reported", "label": "Error report printed: the traceback, then the kind of error and message"},
                {"id": "finished", "label": "The program ends normally"},
            ],
            "initial": "parsing",
            "final": ["reported", "finished"],
            "transitions": [["parsing", "syntaxerror", "the parser encounters a syntax error, such as an IndentationError"], ["syntaxerror", "reported", "Python prints the kind of error and a message"], ["parsing", "executing", "the text is syntactically correct"], ["executing", "executing", "the statement runs; execution reaches the next statement"], ["executing", "exception", "executing a statement raises a NameError, TypeError or ZeroDivisionError"], ["exception", "handled", "the program is written to handle the exception"], ["handled", "executing", "execution continues"], ["exception", "reported", "the exception is not handled: the error stops the program"], ["executing", "finished", "the last statement has been executed"]],
        },
    },
    {
        "id": "InvalidUnitInteraction",
        "pattern": "Interaction",
        "title": "The Dishonest Capacity Calculator meets an invalid unit",
        "concepts": ["UnassignedName", "InputGuard", "NameErrorKind"],
        "also_from": ["WorkedProgram", "DecisionPattern", "CaseInsensitiveTest", "Traceback", "ElifClause", "ElseClause", "ProgramExecution"],
        "read_from": "chapter 2, the Decision pattern section and the Kind of error section: Unassigned name (discrepancy is assigned inside the if clause and the elif clause only; a unit that is neither TB, tb, GB nor gb runs neither clause, and the variable is never created), NameError (name, the missing name in quotation marks, is not defined), Input guard (an else clause displays a message such as You must enter TB or GB and calls sys.exit() to quit the program)",
        "why": "the passage is an exchange between parties in an order that matters - the user types a unit, the program checks its clauses, Python prints an error report, and then the else clause answers the user instead: an interaction",
        "data": {
            "participants": [{"id": "user", "label": "User"}, {"id": "program", "label": "Dishonest Capacity Calculator"}, {"id": "python", "label": "Python error report"}],
            "messages": [
                ["program", "user", "ask for the unit"],
                ["user", "program", "enter an invalid unit, neither TB, tb, GB nor gb"],
                ["program", "program", "the if clause and the elif clause are both skipped"],
                ["program", "program", "the variable discrepancy is never created"],
                ["program", "python", "use the unassigned name discrepancy"],
                ["python", "user", "NameError: name 'discrepancy' is not defined, after the traceback", "reply"],
                ["user", "program", "enter the invalid unit again, with the input guard added"],
                ["program", "program", "neither clause runs, so the else clause executes"],
                ["program", "user", "display the message You must enter TB or GB", "reply"],
                ["program", "program", "call sys.exit() to quit the program"],
            ],
        },
    },
    {
        "id": "TruthValueUses",
        "pattern": "SetOfUses",
        "title": "What a programmer does with truth values and comparisons",
        "concepts": ["BooleanValue", "Truthiness", "Comparison", "BooleanExpression", "Condition"],
        "also_from": ["TruthValue", "Equality", "Ordering", "EqualsVersusAssign", "AndOperator", "OrOperator", "NotOperator", "Toggle", "CaseInsensitiveTest", "IfStatement", "NoneValue"],
        "read_from": "chapter 2, the Truth value, Comparison, Boolean operation and Control structure sections: Boolean value (the type bool has exactly two members, True and False), Truthiness (any object can be tested for truth value, for use in a condition or as an operand of the Boolean operations), Comparison (an expression that asks a question about two values and answers with a Boolean value; ==, !=, <, >, <=, >=), Boolean expression (comparisons and Boolean operators mixed in one expression), Condition (an expression that a flow control statement evaluates to decide what to do), Toggle (flag = not flag)",
        "why": "the passages list what a programmer and a flow control statement do with truth values - compare two values, join or reverse truth values, test any value for truth, write a condition, toggle a Boolean variable - which is a set of uses by actors, not a sequence",
        "data": {
            "system": "TRUTH VALUES AND COMPARISONS",
            "actors": [{"id": "programmer", "label": "Programmer"}, {"id": "statement", "label": "Flow control statement"}],
            "usecases": [
                {"id": "compare", "label": "Ask whether two values are the same with == or different with !="},
                {"id": "order", "label": "Compare two values by size with <, >, <= and >="},
                {"id": "join", "label": "Join two truth values with and or or, reverse one with not"},
                {"id": "mix", "label": "Mix comparisons and Boolean operators in one Boolean expression"},
                {"id": "toggle", "label": "Toggle a Boolean variable: flag = not flag"},
                {"id": "truth", "label": "Test any value for truth: None, zero and empty sequences count as false"},
                {"id": "condition", "label": "Evaluate a condition to decide which block runs"},
                {"id": "skip", "label": "Execute the block when the condition is True, skip it when False"},
            ],
            "links": [["programmer", "compare"], ["programmer", "order"], ["programmer", "join"], ["programmer", "mix"], ["programmer", "toggle"], ["statement", "truth"], ["statement", "condition"], ["statement", "skip"]],
        },
    },
    {
        "id": "FlowControlMap",
        "pattern": "TopicAndParts",
        "title": "Flow control: its parts, its statements and its expression forms",
        "concepts": ["FlowControl", "ControlStructure", "Branching", "ExpressionForm", "PatternMatching"],
        "also_from": ["Condition", "Block", "Indentation", "Clause", "Keyword", "IfStatement", "ElifClause", "ElseClause", "BranchChain", "ConditionalExpression", "AssignmentExpression", "MatchStatement", "CasePattern", "WildcardPattern", "Guard", "Flowchart"],
        "read_from": "chapter 2, the Flow control subject and its sections: Control structure (keyword, condition, colon, indented block called its clause), Branching (the if statement and the elif and else clauses that may follow it), Expression form (the conditional expression x if C else y and the assignment expression name := value), Pattern matching (the match statement with case patterns, the wildcard underscore and guards), Flowchart (diamonds for branching points, rectangles for steps)",
        "why": "the subject classifies one topic, flow control, by the parts a statement is built from, by the statements that choose between blocks, by the forms that bring a choice into an expression and by the modern alternative, and lists the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "Flow control: deciding which instructions run",
            "branches": [
                {"label": "Control structure: the parts of a flow control statement", "children": ["Keyword: if, elif, else, reserved by the language", "Condition: an expression evaluated to decide what to do", "Colon at the end of the first line", "Block: lines grouped by their indentation", "Clause: the header and the block it controls"]},
                {"label": "Branching: the choice between alternative blocks", "children": ["if statement: its block runs when the condition is True", "elif clause: another condition, checked only if earlier ones were False", "else clause: runs when no earlier condition was true", "Branch chain: at most one block runs, exactly one with else"]},
                {"label": "Expression form: a choice inside a single expression", "children": ["Conditional expression: x if C else y", "Assignment expression: name := value, the walrus operator"]},
                {"label": "Pattern matching: the match statement since Python 3.10", "children": ["case pattern: a literal, a capture name or alternatives", "Wildcard pattern: the underscore matches anything", "Guard: if followed by an expression after the pattern"]},
                {"label": "Flowchart: the diagram of the possible paths", "children": ["Diamonds for branching points", "Rectangles for the other steps", "Rounded rectangles for the start and the end"]},
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
