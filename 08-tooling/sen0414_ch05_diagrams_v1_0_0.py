#!/usr/bin/env python3
"""SEN0414, chapter 5 (Debugging, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of the debugging tools a use-case diagram, the life of an exception a state
diagram, an exchange between the program, the logger, the handler and the output stream a sequence diagram, a topic and its parts a mind
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
        "id": "DebuggingABug",
        "pattern": "Workflow",
        "title": "How a programmer finds the root cause of a bug",
        "concepts": ["Debugging", "Bug", "LogicError", "InstrumentChoice"],
        "also_from": ["Tracebacks", "TracebackReading", "SanityCheck", "AssertStatement", "FailFast", "Logging", "Breakpoint", "InspectorPane", "ProgramState"],
        "read_from": "chapter 5, the Nature of a bug and Instrument selection sections: Bug (the gap between the intention in the programmer's head and the behaviour of the running program), Logic error (the program runs to the end and produces a wrong result, and the interpreter is silent), Debugging (finding the root cause, the earliest point where the behaviour departs from the intention), Choosing by question (assert when a belief must hold, log when the run must leave a record, the debugger when the state at one point is the question)",
        "why": "the explanations describe what the programmer does in order - notice the wrong result, read the traceback if there is one, pick the tool built for the question, find the earliest point where the behaviour departs from the intention, remove the bug, run again - a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "notice", "label": "The programmer sees that the result of the running program is wrong"},
                {"id": "reported", "label": "Does the interpreter report the error with a traceback?", "kind": "decision"},
                {"id": "readtb", "label": "Read the traceback: the file, the line and the function that raised"},
                {"id": "belief", "label": "Must a condition the programmer believes in hold at one point?", "kind": "decision"},
                {"id": "assert", "label": "Write an assert statement as a sanity check: the program fails fast"},
                {"id": "record", "label": "Must the run leave a record of which values the variables held?", "kind": "decision"},
                {"id": "log", "label": "Add logging calls that record when execution reached a call"},
                {"id": "debug", "label": "Run the program under the debugger and pause at a breakpoint"},
                {"id": "inspect", "label": "Inspect the values in the variables while the code runs"},
                {"id": "cause", "label": "Find the root cause: the earliest point where the behaviour departs"},
                {"id": "fix", "label": "Remove the bug and run the program again"},
                {"id": "right", "label": "Is the result right now?", "kind": "decision"},
            ],
            "flows": [["start", "notice"], ["notice", "reported"], ["reported", "readtb", "yes"], ["reported", "belief", "no: a logic error, the interpreter is silent"], ["readtb", "belief"], ["belief", "assert", "yes"], ["belief", "record", "no"], ["record", "log", "yes"], ["record", "debug", "no: the state at one point is the question"], ["debug", "inspect"], ["assert", "cause"], ["log", "cause"], ["inspect", "cause"], ["cause", "fix"], ["fix", "right"], ["right", "belief", "no"], ["right", "end", "yes"]],
        },
    },
    {
        "id": "SteppingThrough",
        "pattern": "Workflow",
        "title": "Stepping through a program under the debugger",
        "concepts": ["RunUnderDebugger", "Breakpoint", "StepIn", "StepOver", "StepOut", "ContinueControl"],
        "also_from": ["Controls", "StopControl", "InspectorPane", "ProgramState", "PdbCommands"],
        "read_from": "chapter 5, the Debugger interface and Controls sections: Running under the debugger (the Debug button starts the program paused just before its first line), Debug Inspector pane (the current value of each variable), Breakpoint (a mark on a line that makes the debugger pause whenever the program reaches it), Continue (execute normally until a breakpoint or the end), Step In (execute the next line, pausing on the first line of a called function), Step Over (run the called function at full speed), Step Out (run until the current function returns), Stop (terminate the program)",
        "why": "the passage is a procedure the programmer repeats - look at the paused program, decide how far it should run before it stops again, press the control for that, look again - with every control answering one question about how far: a workflow",
        "data": {
            "nodes": [
                {"id": "debugbtn", "label": "Click the Debug button: the program is paused before its first line"},
                {"id": "inspect", "label": "Read the current value of each variable in the Debug Inspector pane"},
                {"id": "answered", "label": "Is the question about the state of the program answered?", "kind": "decision"},
                {"id": "finish", "label": "Click Stop to terminate the program, or Continue to let it run normally"},
                {"id": "far", "label": "Should the program run at normal speed until the next breakpoint?", "kind": "decision"},
                {"id": "cont", "label": "Continue: the program executes normally until it reaches a breakpoint"},
                {"id": "reached", "label": "Did the program reach a breakpoint before it terminated?", "kind": "decision"},
                {"id": "call", "label": "Is the next line a function call?", "kind": "decision"},
                {"id": "inside", "label": "Should the debugger pause inside the called function?", "kind": "decision"},
                {"id": "stepin", "label": "Step In: execute the next line, pause on a called function's first line"},
                {"id": "stepover", "label": "Step Over: the called function runs at full speed, pause on return"},
                {"id": "leave", "label": "Has Step In entered a function that is no longer of interest?", "kind": "decision"},
                {"id": "stepout", "label": "Step Out: execute lines at full speed until the current function returns"},
            ],
            "flows": [["start", "debugbtn"], ["debugbtn", "inspect"], ["inspect", "answered"], ["answered", "finish", "yes"], ["answered", "far", "no"], ["finish", "end"], ["far", "cont", "yes"], ["far", "call", "no: one line at a time"], ["cont", "reached"], ["reached", "inspect", "yes"], ["reached", "end", "no: the program ran to its end"], ["call", "inside", "yes"], ["call", "stepin", "no"], ["inside", "stepin", "yes"], ["inside", "stepover", "no"], ["stepin", "leave"], ["leave", "stepout", "yes"], ["leave", "inspect", "no"], ["stepover", "inspect"], ["stepout", "inspect"]],
        },
    },
    {
        "id": "ExceptionLife",
        "pattern": "LifeCycle",
        "title": "The life of an exception, from raise to except or traceback",
        "concepts": ["RaiseStatement", "ExceptionUnwinding", "UnhandledException", "Tracebacks"],
        "also_from": ["ErrorSignalling", "Raising", "ExceptionClass", "ExceptionMessage", "ArgumentValidation", "TracebackReading", "StandardErrorStream"],
        "read_from": "chapter 5, the Raising and Tracebacks sections: Error signalling (an exception is an object that carries a description of the problem and travels up through the running code until something handles it), Raise statement (stop running this code and move the execution to the except statement), Exception unwinding (the exception leaves the function and arrives in the caller, repeated until an except clause matches or the stack is empty), Unhandled exception (the program crashes and displays the error message), Tracebacks (the report Python prints on the error stream)",
        "why": "the explanations describe the states an exception is in - not yet raised, raised, travelling up the call stack, caught, unhandled - and the events that move it from one to the next: a life cycle",
        "data": {
            "states": [
                {"id": "running", "label": "Code running normally: no exception"},
                {"id": "raised", "label": "Raised: an object carrying a description of the problem"},
                {"id": "travelling", "label": "Travelling up the call stack: leaves the function, arrives in the caller"},
                {"id": "caught", "label": "Caught: an except clause matches the exception and handles it"},
                {"id": "crashed", "label": "Unhandled: the program crashes and Python prints a traceback on stderr"},
            ],
            "initial": "running",
            "final": ["crashed"],
            "transitions": [["running", "raised", "a raise statement, or Python tries to execute invalid code"], ["raised", "caught", "try and except statements cover the raise statement"], ["raised", "travelling", "the function does not handle it"], ["travelling", "travelling", "the caller does not handle it either: the process is repeated"], ["travelling", "caught", "an except clause matches the exception class"], ["travelling", "crashed", "the stack is empty: no except clause matches"], ["caught", "running", "the except clause shows the message written for the user"]],
        },
    },
    {
        "id": "LoggingInteraction",
        "pattern": "Interaction",
        "title": "A log call travels from the program to the screen or a file",
        "concepts": ["Logger", "Handler", "LogRecord", "BasicConfig"],
        "also_from": ["Setup", "LogFormat", "LogToFile", "LevelThreshold", "LoggingLevels", "DefaultLevel", "DisablingLogging", "StandardErrorStream", "Logging"],
        "read_from": "chapter 5, the Setup and Loggers and handlers sections: Basic config (creates a StreamHandler with a default Formatter and adds it to the root logger; level, format and filename), Logger (the object on which log calls are made), Log record (created for each event: logger name, level, message, line number), Handler (delivers the record to a destination: a StreamHandler writes to sys.stderr, a FileHandler to a disk file), Level threshold (messages below the level are ignored), Disabling logging (logging.disable(logging.CRITICAL) suppresses all messages)",
        "why": "the passage is an exchange of messages between parties in an order that matters - the program configures, the logger creates a record and checks its level, the handler formats it and writes it to the stream or the file: an interaction",
        "data": {
            "participants": [{"id": "program", "label": "Program"}, {"id": "logger", "label": "Root logger"}, {"id": "handler", "label": "StreamHandler or FileHandler"}, {"id": "stream", "label": "Screen (stderr) or text file"}],
            "messages": [
                ["program", "logger", "logging.basicConfig(level=logging.DEBUG, format=..., filename=...)"],
                ["logger", "handler", "create a StreamHandler with a default Formatter for the root logger"],
                ["program", "logger", "logging.debug('Start of program')"],
                ["logger", "logger", "is the level of the message at least the threshold? below it, ignore it"],
                ["logger", "handler", "a log record: logger name, level, message, line number of the call"],
                ["handler", "handler", "format the record: %(asctime)s - %(levelname)s - %(message)s"],
                ["handler", "stream", "write the line to sys.stderr, or to the file myProgramLog.txt"],
                ["stream", "program", "the log message is displayed on the screen or saved to the text file", "reply"],
                ["program", "logger", "logging.disable(logging.CRITICAL)"],
                ["logger", "logger", "suppress all log messages: calls of that severity and below are disabled"],
            ],
        },
    },
    {
        "id": "InstrumentUses",
        "pattern": "SetOfUses",
        "title": "Who uses the debugging tools, and for what",
        "concepts": ["InstrumentSelection", "InstrumentChoice", "AssertVersusRaise", "LoggingVersusPrint"],
        "also_from": ["SanityCheck", "AssertStatement", "FailFast", "RaiseStatement", "UnhandledException", "Tracebacks", "TracebackReading", "Logging", "DisablingLogging", "Debugger", "Debugging"],
        "read_from": "chapter 5, the Instrument selection section and the two comparisons: assertions, exceptions, logging and the debugger are all valuable tools to find and prevent bugs; assert when the programmer's belief must hold, raise when the caller can react to the error, log when the run must leave a record, the debugger when the state at one point is the question; log messages are for the programmer and print is for the user; the interpreter prints a traceback when no except clause matches",
        "why": "the passage lists what the programmer, the user and the interpreter do with the four tools - assert, raise, catch, log, step, read a traceback - which is a set of uses by actors, not a sequence",
        "data": {
            "system": "THE DEBUGGING TOOLS",
            "actors": [{"id": "programmer", "label": "Programmer"}, {"id": "user", "label": "User"}, {"id": "interpreter", "label": "Python interpreter"}],
            "usecases": [
                {"id": "assert", "label": "Write an assert statement as a sanity check that a condition holds"},
                {"id": "raise", "label": "Raise an exception when the caller can react to the error"},
                {"id": "catch", "label": "Catch the exception with try and except statements"},
                {"id": "log", "label": "Add logging calls that record which values the variables held"},
                {"id": "disable", "label": "Switch all log messages off with logging.disable"},
                {"id": "step", "label": "Step through the program one line at a time in the debugger"},
                {"id": "readtb", "label": "Read the traceback to find the line where the exception was raised"},
                {"id": "seemsg", "label": "See an error message written with print, such as File not found"},
                {"id": "invalid", "label": "Type invalid data: an error the program meets in normal operation"},
                {"id": "printtb", "label": "Print a traceback on the error stream when no except clause matches"},
                {"id": "raiseself", "label": "Raise an exception whenever it tries to execute invalid code"},
            ],
            "links": [["programmer", "assert"], ["programmer", "raise"], ["programmer", "catch"], ["programmer", "log"], ["programmer", "disable"], ["programmer", "step"], ["programmer", "readtb"], ["user", "seemsg"], ["user", "invalid"], ["interpreter", "printtb"], ["interpreter", "raiseself"]],
        },
    },
    {
        "id": "LoggingLevelsMap",
        "pattern": "TopicAndParts",
        "title": "Logging levels: the five ranks, the threshold and disabling",
        "concepts": ["Levels", "LoggingLevels", "LevelThreshold", "DefaultLevel", "DisablingLogging"],
        "also_from": ["BasicConfig", "Setup", "Logging", "LoggingVersusPrint"],
        "read_from": "chapter 5, the Levels section: Logging levels (DEBUG, INFO, WARNING, ERROR and CRITICAL, 10 to 50, each with a function of the same name), Level threshold (set with the level argument of basicConfig; messages of that level and above are emitted), Default level (WARNING when logging is not configured), Disabling logging (logging.disable(logging.CRITICAL) suppresses all log messages; NOTSET turns them back on)",
        "why": "the section classifies one topic, the importance of a log message, by the five ranks, by the threshold that filters them and by the switch that disables them, and lists the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "Logging levels: categorising log messages by importance",
            "branches": [
                {"label": "The five levels, from the least to the most important", "children": ["DEBUG, 10: logging.debug()", "INFO, 20: logging.info()", "WARNING, 30: logging.warning()", "ERROR, 40: logging.error()", "CRITICAL, 50: logging.critical()"]},
                {"label": "The threshold: the level below which messages are ignored", "children": ["Set with the level argument of basicConfig", "Messages of that level and above are emitted", "Default level WARNING when logging is not configured", "Raising the threshold hides the lower levels without deleting any call"]},
                {"label": "Disabling: switching messages off from one place", "children": ["logging.disable(logging.CRITICAL) suppresses all log messages", "NOTSET, 0, turns them back on", "The calls stay in the program; none has to be deleted"]},
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
