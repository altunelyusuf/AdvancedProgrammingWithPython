#!/usr/bin/env python3
"""SEN0414, chapter 1 (Python basics, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of the interactive shell a use-case diagram, the life of a variable binding a state
diagram, an exchange between the user, the shell and the interpreter a sequence diagram, a topic and its parts a mind
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
        "id": "ExpressionEvaluation",
        "pattern": "Workflow",
        "title": "How the interpreter evaluates an expression",
        "concepts": ["Expression", "Operator", "Precedence", "InteractiveShell"],
        "also_from": ["Value", "DataType", "Concatenation", "Replication", "TextOperation"],
        "read_from": "chapter 1, Entering Expressions into the Interactive Shell: Expression (a piece of code that evaluates to a value, built from literals, names, operators and function calls), Operator (the symbol between its operands; the type of the operands decides its meaning), Precedence (** first, then *, /, //, %, then + and -; parentheses override it)",
        "why": "the explanations describe what Python does with an expression in order - read it, decide which operator applies first, apply it, repeat until one value is left - with the type of the operands deciding the meaning on the way: a workflow",
        "data": {
            "nodes": [
                {"id": "type", "label": "The learner types an expression at the prompt, such as 2 + 3 * 6"},
                {"id": "several", "label": "Does the expression contain several operators?", "kind": "decision"},
                {"id": "parens", "label": "Do parentheses override the order?", "kind": "decision"},
                {"id": "inner", "label": "Apply the operator between the parentheses first"},
                {"id": "prec", "label": "Apply ** first, then *, /, // and %, then + and -"},
                {"id": "strings", "label": "Are the operands strings?", "kind": "decision"},
                {"id": "text", "label": "+ joins the strings and * repeats them"},
                {"id": "arith", "label": "The operator calculates with the numbers"},
                {"id": "value", "label": "The expression evaluates to one value, such as 20"},
                {"id": "show", "label": "The shell shows the result at once"},
            ],
            "flows": [["start", "type"], ["type", "several"], ["several", "parens", "yes"], ["several", "strings", "no"], ["parens", "inner", "yes"], ["parens", "prec", "no"], ["inner", "strings"], ["prec", "strings"], ["strings", "text", "yes"], ["strings", "arith", "no"], ["text", "value"], ["arith", "value"], ["value", "show"], ["show", "end"]],
        },
    },
    {
        "id": "ShellUses",
        "pattern": "SetOfUses",
        "title": "Who uses the interactive shell, and for what",
        "concepts": ["InteractiveEnvironment", "InteractiveShell", "PythonInterpreter"],
        "also_from": ["Expression", "Output", "Input", "PythonVersion", "DataType", "FunctionCall"],
        "read_from": "chapter 1, the Execution environment branch: Interactive environment (a learner types Python and sees the result immediately), Interactive shell (statements and expressions at a prompt; the read-eval-print loop), Python interpreter (reads Python code and runs it, line by line in the shell or from a file), Python version (python --version)",
        "why": "the passage lists what a learner and the interpreter do with the shell - type expressions, see results, run statements, read the type of a value, run a file - which is a set of uses by actors, not a sequence",
        "data": {
            "system": "THE INTERACTIVE SHELL",
            "actors": [{"id": "learner", "label": "Learner"}, {"id": "interpreter", "label": "Python interpreter"}],
            "usecases": [
                {"id": "typeexpr", "label": "Type an expression at the prompt"},
                {"id": "see", "label": "See the result immediately"},
                {"id": "statement", "label": "Enter a statement, such as spam = 42"},
                {"id": "typeof", "label": "Read the type of a value with the type function"},
                {"id": "call", "label": "Call a function such as print or input"},
                {"id": "read", "label": "Read each expression as soon as it is entered"},
                {"id": "eval", "label": "Evaluate it and print the result: the read-eval-print loop"},
                {"id": "file", "label": "Run a source file directly, without creating an executable"},
            ],
            "links": [["learner", "typeexpr"], ["learner", "see"], ["learner", "statement"], ["learner", "typeof"], ["learner", "call"], ["interpreter", "read"], ["interpreter", "eval"], ["interpreter", "file"]],
        },
    },
    {
        "id": "VariableBindingLife",
        "pattern": "LifeCycle",
        "title": "The life of a variable binding",
        "concepts": ["BindingOperation", "Variable", "Assignment"],
        "also_from": ["Value", "Integer", "Expression"],
        "read_from": "chapter 1, the Binding operation section: Binding operation (gives a value a name so that later lines can refer to it), Variable (a name that refers to a value stored in memory; assigning to the name again makes it refer to a new value), Assignment (spam = 42 binds the name on the left to the value of the expression on the right)",
        "why": "the explanations describe states a name is in - not yet bound, referring to a value, referring to a new value - and the statements that move it between them: a life cycle",
        "data": {
            "states": [
                {"id": "unbound", "label": "Name not yet used: no value stored"},
                {"id": "bound", "label": "Name refers to a value stored in memory"},
                {"id": "rebound", "label": "Name refers to a new value"},
            ],
            "initial": "unbound",
            "final": ["rebound"],
            "transitions": [["unbound", "bound", "assignment statement: spam = 42"], ["bound", "bound", "later lines refer to the name wherever the value is needed"], ["bound", "rebound", "assigning to the name again"], ["rebound", "rebound", "assigning to the name again"]],
        },
    },
    {
        "id": "ProgramInteraction",
        "pattern": "Interaction",
        "title": "A program talks to its user through the shell and the interpreter",
        "concepts": ["IOFunction", "Output", "Input", "FunctionCall"],
        "also_from": ["InteractiveShell", "PythonInterpreter", "Bytecode", "TypeConversion", "Length", "String", "Expression"],
        "read_from": "chapter 1: Input-output function (print sends text out, input reads text in), Output (print('Hello, world!') displays the text and moves to a new line), Input (waits for the user to type a line and returns it; writes the prompt first), Function call (the call evaluates to the return value), Python interpreter and Bytecode (source compiled into bytecode and executed)",
        "why": "the passage is an exchange of messages between parties - the user, the shell and the interpreter - in an order that matters: an interaction",
        "data": {
            "participants": [{"id": "user", "label": "User"}, {"id": "shell", "label": "Interactive shell"}, {"id": "interp", "label": "Python interpreter"}],
            "messages": [
                ["user", "shell", "type print('Hello, world!') at the prompt"],
                ["shell", "interp", "read the function call"],
                ["interp", "interp", "compile the source code into bytecode and execute it"],
                ["interp", "shell", "the print function writes Hello, world! as text", "reply"],
                ["shell", "user", "display Hello, world! and move to a new line", "reply"],
                ["user", "shell", "type input('What is your name?')"],
                ["shell", "user", "write the prompt text first, without a trailing newline", "reply"],
                ["user", "shell", "type a line, such as Alice"],
                ["shell", "interp", "the input function returns the line as a string"],
                ["interp", "shell", "the call evaluates to its return value", "reply"],
            ],
        },
    },
    {
        "id": "ValueModelMap",
        "pattern": "TopicAndParts",
        "title": "The value model: data types, expressions and conversions",
        "concepts": ["Value", "ValueModel", "DataType", "Expression", "Integer", "FloatingPoint", "String"],
        "also_from": ["TypeConversion", "NumericValue", "TextValue"],
        "read_from": "chapter 1, the Value branch: Value (42, 3.14 and 'Alice' each have a data type), Numeric value (integers and floating-point numbers), Text value (String, type str), Value model (every value has a data type; an expression evaluates to a value), Expression (literals, names, operators and function calls), Type conversion (int('42'), float('3.5'), str(29))",
        "why": "the branch classifies one topic, the value, by its data types, by what an expression is built from and by how a value is converted, and lists the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "The value model",
            "branches": [
                {"label": "Data type: the kind of a value", "children": ["Integer: int, a whole number such as 42", "Floating point: float, a fractional part such as 3.14", "String: str, characters between quotes such as 'Alice'"]},
                {"label": "Expression: code that evaluates to a value", "children": ["Literals", "Names", "Operators", "Function calls", "2 + 3 * 6 evaluates to 20"]},
                {"label": "Type conversion: a value of another type", "children": ["int('42') gives the integer 42", "float('3.5') gives the float 3.5", "str(29) gives the string '29'"]},
            ],
        },
    },
    {
        "id": "RunningAProgram",
        "pattern": "Workflow",
        "title": "How CPython runs a program",
        "concepts": ["PythonImplementation", "PythonInterpreter", "CPython", "Bytecode", "GlobalInterpreterLock", "FreeThreadedBuild"],
        "also_from": ["InterpreterBuild", "Thread"],
        "read_from": "chapter 1, the Python implementation and Interpreter build sections: Python interpreter (reads source code and runs it without creating an executable first), CPython (the canonical implementation), Bytecode (source compiled into bytecode, executed by a virtual machine), Global interpreter lock (only one thread executes bytecode at a time), Free-threaded build (--disable-gil: multiple threads run bytecode simultaneously)",
        "why": "the explanations describe a procedure in order - read the source, compile it into bytecode, execute it on the virtual machine - with one choice fixed by the build, whether one thread or several may run bytecode at a time: a workflow",
        "data": {
            "nodes": [
                {"id": "read", "label": "The interpreter reads the Python source code"},
                {"id": "compile", "label": "The source code is compiled into bytecode"},
                {"id": "build", "label": "Is this the free-threaded build, configured with --disable-gil?", "kind": "decision"},
                {"id": "gil", "label": "The GIL ensures that only one thread executes bytecode at a time"},
                {"id": "free", "label": "Multiple threads run bytecode simultaneously in the same interpreter"},
                {"id": "vm", "label": "The virtual machine executes the machine code for each bytecode"},
            ],
            "flows": [["start", "read"], ["read", "compile"], ["compile", "build"], ["build", "free", "yes"], ["build", "gil", "no"], ["gil", "vm"], ["free", "vm"], ["vm", "end"]],
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
