#!/usr/bin/env python3
"""SEN0414, chapter 19 (Keeping Time, Scheduling Tasks, and Launching Programs, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case
diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts
whose explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects. Every element label is made of words that occur in the first paragraph
and the definition of the accompanying concepts or their section, which is the text the page shows; run_checks() measures
that (the grounding ratio, required here to be 0.84 or more) besides the structural rules. This module follows the layout of
sen0414_ch18_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another
chapter is not edited); because chapter 19 has no page data yet, nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_5
document and ABox, so the grounding can be measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch19_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "TimingALapOfTheStopwatch",
        "pattern": "Workflow",
        "title": "Project 14: the Super Stopwatch times each lap",
        "concepts": ["LapArithmetic", "RoundFunction", "SteppedWallClock", "ColumnFormatting"],
        "also_from": ["SuperStopwatch", "ClockKinds", "SleepFunction", "ProfilingByClock"],
        "read_from": "chapter 19, Project 14: note the start time, wait for ENTER, subtract the last reading to get the lap time, round both times to two digits "
                     "and print the lap number, the total time and the lap time",
        "why": "the passage is a numbered sequence of steps that repeats for each lap and ends on one test, whether the user has pressed Ctrl-C: a workflow",
        "data": {
            "nodes": [
                {"id": "t0", "label": "Note the start time with time.time()"},
                {"id": "wait", "label": "Wait for the user to press ENTER"},
                {"id": "lap", "label": "Subtract the last time to get the lap time"},
                {"id": "round", "label": "Round the lap time and the total time to two digits"},
                {"id": "print", "label": "Print the lap number, the total time and the lap time"},
                {"id": "quit", "label": "Did the user press Ctrl-C?", "kind": "decision"},
            ],
            "flows": [["start", "t0"], ["t0", "wait"], ["wait", "lap"], ["lap", "round"], ["round", "print"], ["print", "quit"],
                      ["quit", "wait", "no"], ["quit", "end", "yes"]],
        },
    },
    {
        "id": "WaitingUntilADate",
        "pattern": "Workflow",
        "title": "Pausing a program until a specific date",
        "concepts": ["PollingLoops", "SleepFunction", "SleepDrift", "DatetimeComparison"],
        "also_from": ["PausingPrograms", "MomentsAndFields", "CurrentMoment", "ClockInfoTable"],
        "read_from": "chapter 19, Pausing Until a Specific Date: make a datetime for the date, loop while datetime.now() is earlier, and call time.sleep(1) "
                     "on each pass so that the computer does not waste processor time",
        "why": "the passage is a loop with one test and a step that repeats until the test changes its answer: a workflow",
        "data": {
            "nodes": [
                {"id": "make", "label": "Make a datetime for the date"},
                {"id": "now", "label": "Read the current moment with datetime.now()"},
                {"id": "later", "label": "Is the current moment earlier than the date?", "kind": "decision"},
                {"id": "sleep", "label": "Pause the program with time.sleep(1)"},
                {"id": "go", "label": "Continue with the rest of the program"},
            ],
            "flows": [["start", "make"], ["make", "now"], ["now", "later"], ["later", "sleep", "yes"], ["sleep", "now"], ["later", "go", "no"], ["go", "end"]],
        },
    },
    {
        "id": "ChoosingHowToLaunchAProgram",
        "pattern": "Workflow",
        "title": "Launching another program from Python",
        "concepts": ["RunWaits", "PopenNoWait", "ArgumentList", "ShellInjection", "CheckAndTimeout"],
        "also_from": ["RunAndPopen", "ArgumentsAndOutput", "LaunchingPrograms", "ShellTrueList", "CaptureOutput"],
        "read_from": "chapter 19, Launching Other Programs from Python: pass a list of strings to subprocess.run(), which waits, or to subprocess.Popen(), "
                     "which returns at once, and read the output with capture_output=True",
        "why": "the passage walks through the choices that decide how a program is launched, each answered by yes or no, with the step that follows: a workflow",
        "data": {
            "nodes": [
                {"id": "list", "label": "Put the program and its arguments in a list of strings"},
                {"id": "wait", "label": "Does the program wait for the process to end?", "kind": "decision"},
                {"id": "run", "label": "Call subprocess.run() with the list"},
                {"id": "popen", "label": "Call subprocess.Popen() with the list"},
                {"id": "poll", "label": "Call poll(), which returns None while the process runs"},
                {"id": "capture", "label": "Pass capture_output=True and text=True to get the output"},
                {"id": "check", "label": "Pass check=True and a timeout to raise on a failure"},
            ],
            "flows": [["start", "list"], ["list", "wait"], ["wait", "run", "yes"], ["wait", "popen", "no"], ["run", "capture"], ["capture", "check"],
                      ["popen", "poll"], ["poll", "end"], ["check", "end"]],
        },
    },
    {
        "id": "ARunningAChildProcess",
        "pattern": "Interaction",
        "title": "A program starting a process with Popen and waiting for it",
        "concepts": ["PopenNoWait", "ExitCodes", "TerminateVsKill", "RunWaits"],
        "also_from": ["RunAndPopen", "ExitAndStopping", "LaunchingPrograms", "CheckAndTimeout"],
        "read_from": "chapter 19, Popen: subprocess.Popen() returns a Popen object at once, poll() returns None while the process runs and its exit code afterwards, "
                     "and wait() blocks until the process ends",
        "why": "the passage is an exchange between the program, the Popen object and the process in an order that matters - each call returns "
               "what the next call needs: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "popen", "label": "The Popen object"},
                {"id": "proc", "label": "The process"},
            ],
            "messages": [
                ["prog", "popen", "Calls subprocess.Popen() with a list"],
                ["popen", "proc", "Starts the process"],
                ["popen", "prog", "Returns the Popen object at once", "reply"],
                ["prog", "popen", "Calls poll()"],
                ["popen", "prog", "Returns None while the process runs", "reply"],
                ["prog", "popen", "Calls wait()"],
                ["proc", "popen", "Ends with an exit code"],
                ["popen", "prog", "Returns the exit code", "reply"],
            ],
        },
    },
    {
        "id": "ALaunchedProcessFromStartToExit",
        "pattern": "LifeCycle",
        "title": "A launched process from the start to its exit",
        "concepts": ["PopenNoWait", "ExitCodes", "TerminateVsKill", "CheckAndTimeout"],
        "also_from": ["RunAndPopen", "ExitAndStopping", "RunWaits", "LaunchingPrograms"],
        "read_from": "chapter 19, Popen: a process is started, runs while poll() returns None, and ends with an exit code; the Python documentation adds the signals "
                     "that stop it",
        "why": "the passage follows one process through the states it can be in and names the event that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "started", "label": "A process started by Popen"},
                {"id": "running", "label": "A running process"},
                {"id": "exited", "label": "A process that exited with a return code"},
                {"id": "killed", "label": "A process ended by a signal"},
            ],
            "initial": "started",
            "final": ["exited", "killed"],
            "transitions": [
                ["started", "running", "Popen returns and poll() gives None"],
                ["running", "exited", "The program ends and poll() gives its exit code"],
                ["running", "killed", "kill() sends SIGKILL and the return code is -9"],
                ["running", "exited", "terminate() sends SIGTERM and a handler exits with 0"],
                ["running", "killed", "A timeout expires and run() kills the child"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithDatetime",
        "pattern": "SetOfUses",
        "title": "What a program can do with moments and durations in datetime",
        "concepts": ["DatetimeObject", "CurrentMoment", "DatetimeComparison", "DurationArithmetic", "StrftimeFormat", "StrptimeParse", "ZoneInfoZones"],
        "also_from": ["DatetimeValues", "MomentsAndFields", "DurationsTimedelta", "FormatAndParse", "ZoneAwareness", "NoMonthsOrYears", "IsoFormats"],
        "read_from": "chapter 19, the datetime module: the module makes a moment, reads the current moment, compares two moments, adds a duration, "
                     "turns a moment into text with strftime() and reads text into a moment with strptime()",
        "why": "the chapter lists independent things a program can do with the same module - make, read, compare, add, format, parse - "
               "a set of uses of the same module, not a sequence",
        "data": {
            "system": "THE DATETIME MODULE",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "make", "label": "Make a moment from a year, month and day"},
                {"id": "now", "label": "Read the current moment"},
                {"id": "compare", "label": "Compare two moments"},
                {"id": "add", "label": "Add a duration to a moment"},
                {"id": "format", "label": "Turn a moment into text with strftime()"},
                {"id": "parse", "label": "Read text into a moment with strptime()"},
                {"id": "zone", "label": "Attach a time zone with ZoneInfo"},
            ],
            "links": [["prog", "make"], ["prog", "now"], ["prog", "compare"], ["prog", "add"], ["prog", "format"], ["prog", "parse"], ["prog", "zone"]],
        },
    },
    {
        "id": "WhatAProgramCanDoToRunALaterJob",
        "pattern": "SetOfUses",
        "title": "What a program can do to run a job later",
        "concepts": ["CronFields", "TimerThread", "SchedModule", "AsyncioCallLater", "ScheduleLibrary", "LaunchdPlist", "SystemdCalendar"],
        "also_from": ["SchedulingTasks", "OsSchedulers", "InProcessScheduling", "CronEnvironment", "PollingLoops"],
        "read_from": "chapter 19, Running Task Scheduler, launchd, and cron: the operating system schedulers run a program at a time, and the standard "
                     "library runs a function later inside a running program",
        "why": "the chapter lists independent things a program can do to run something later - a cron entry, a timer, a queue of events - "
               "a set of uses of the same need, not a sequence",
        "data": {
            "system": "A JOB THAT RUNS LATER",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "cron", "label": "Write a cron entry with five time fields"},
                {"id": "timer", "label": "Call a function once after a delay with Timer"},
                {"id": "sched", "label": "Order events by time and priority with sched"},
                {"id": "asyncio", "label": "Call a function later with call_later"},
                {"id": "schedule", "label": "Run jobs every day with the schedule package"},
                {"id": "plist", "label": "Describe a job in a launchd property list"},
                {"id": "systemd", "label": "Normalise a systemd calendar expression"},
            ],
            "links": [["prog", "cron"], ["prog", "timer"], ["prog", "sched"], ["prog", "asyncio"], ["prog", "schedule"], ["prog", "plist"], ["prog", "systemd"]],
        },
    },
    {
        "id": "KeepingTimeAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Keeping time, scheduling tasks, and launching programs at a glance: six branches",
        "concepts": ["EpochClock", "DatetimeValues", "TimeZonesAndPitfalls", "LaunchingPrograms", "SchedulingTasks", "BookAndPractice"],
        "also_from": ["EpochTimestamp", "ClockKinds", "PausingPrograms", "MomentsAndFields", "DurationsTimedelta", "FormatAndParse", "ZoneAwareness", "DaylightSaving",
                      "LimitsOfTime", "RunAndPopen", "ArgumentsAndOutput", "OsSchedulers", "InProcessScheduling", "ListingsAsPrinted", "PracticePrograms",
                      "Year2038", "WallClockArithmetic", "YearlessParsing", "TwoDigitYear", "NoMonthsOrYears", "EnDashListings", "FridayBackward", "CronEnvironment", "CronFields", "ShellTrueList", "OpenCommand", "SteppedWallClock", "SleepFunction", "TimerThread", "SchedModule", "LapArithmetic", "NaiveVersusAware"],
        "read_from": "chapter 19, the opening of each of its main branches: the clock, the datetime module, time zones, launching programs, "
                     "scheduling, and the book and its practice programs",
        "why": "the chapter classifies one topic, working with time and programs, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "A program reads time, waits, launches and schedules other programs",
            "branches": [
                {"label": "The epoch and the clock",
                 "children": ["The epoch is 1970 in UTC",
                              "A monotonic clock gives the true difference",
                              "Sleep waits at least the time asked"]},
                {"label": "The datetime module",
                 "children": ["A timedelta has no months",
                              "A two-digit year maps 69 to 1969",
                              "A date with no year uses 1900"]},
                {"label": "Time zones",
                 "children": ["A naive value has no zone",
                              "A day across the change is 23 hours",
                              "A signed 32-bit count ends in 2038"]},
                {"label": "Launching programs",
                 "children": ["run() waits and Popen does not",
                              "A list of arguments passes through no shell",
                              "start and open are not on Linux"]},
                {"label": "Scheduling",
                 "children": ["Cron has five time fields",
                              "A cron job does not run in the shell",
                              "sched and Timer run inside a Python process"]},
                {"label": "The book and practice",
                 "children": ["Four places write an en dash",
                              "The stopwatch prints the laps",
                              "Friday the 13th has 688 in 400 years"]},
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
            if n and h / n < MIN_GROUNDING: bad.append("%s: grounding %d/%d below %.2f; words not in the concepts' explanations: %s" % (d["id"], h, n, MIN_GROUNDING, ", ".join(miss)))
    return bad


def nodes_from_ttl(root):
    """the chapter's nodes read from the v1_0_5 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch19#"
    d = os.path.join(root, "03-materials", "ch19", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch19_document_v1_0_5.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch19_domain_abox_v1_0_5.ttl"))
    nodes = {}
    for s in g.subjects(DOC.sectionTitle, None):
        if not str(s).startswith(CHX + "S_"): continue
        cid = str(s)[len(CHX) + 2:]
        body = str(g.value(s, SKOS.definition) or "")
        nodes[cid] = {"id": cid, "label": str(g.value(s, RDFS.label)), "body": body.split("\n\n")[0], "definition": "", "parent": None, "_s": s}
    for cid, n in nodes.items():
        for p in list(g.subjects(DOC.hasSection, n["_s"])) + list(g.objects(n["_s"], DOC.hasParentSection)):
            q = str(p)[len(CHX) + 2:]
            if q in nodes: n["parent"] = q
        x = a.value(URIRef(CHX + "X_" + cid), SKOS.definition)
        if x: n["definition"] = str(x)
        del n["_s"]
    return list(nodes.values())


if __name__ == "__main__":
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    nodes = nodes_from_ttl(os.path.dirname(here))
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-26s %-12s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams, nodes %d" % (len(DIAGRAMS), len(nodes))); sys.exit(1 if bad else 0)
