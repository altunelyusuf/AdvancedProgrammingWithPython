#!/usr/bin/env python3
"""SEN0414, chapter 25 (the Threads subject: the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of a thing a state
diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram type lives in
the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl). Each entry names the concepts whose paragraphs it accompanies, the
narrative pattern, the passage it was read from, one sentence saying why the pattern fits, and the content in the element names the renderer expects. Every element
label is made of words that occur in the first paragraph and the definition of the accompanying concepts or their section; run_checks() measures that (the grounding
ratio, required to be 0.84 or more) besides the structural rules. The helper functions are those of sen0414_ch24_diagrams_v1_0_0.py, written again because a file of
another chapter is not edited; nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_0 document and ABox.

Usage: python3 sen0414_ch25_diagrams_v1_0_0.py   (measures the grounding on the RDODI files of the chapter)
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "StartingAndJoiningAThread",
        "pattern": "Workflow",
        "title": "Starting a thread and waiting for it with join()",
        "concepts": ["StartAThread", "JoinWaits", "PrintedListingJoinFails", "ProgramWaitsForThreads"],
        "also_from": ["StartingThreads", "JoiningThreads", "JoinBeforeStart"],
        "read_from": "chapter 17 of the 2nd edition, Multithreading: create a Thread object with a target, call start(), let the main thread go on and call join() to wait",
        "why": "the passage is a sequence of steps with one test on whether start() was called before join() that sends the program on or to an error: a workflow",
        "data": {
            "nodes": [
                {"id": "make", "label": "Create a Thread object with a target"},
                {"id": "call", "label": "Call start() on the thread"},
                {"id": "go", "label": "The main thread goes on"},
                {"id": "chk", "label": "Was start() called before join()?", "kind": "decision"},
                {"id": "join", "label": "join() waits until the thread has finished"},
                {"id": "err", "label": "join() raises RuntimeError"},
            ],
            "flows": [["start", "make"], ["make", "call"], ["call", "go"], ["go", "chk"], ["chk", "join", "yes"], ["chk", "err", "no"], ["join", "end"], ["err", "end"]],
        },
    },
    {
        "id": "ChoosingBetweenTheTools",
        "pattern": "Workflow",
        "title": "Choosing a tool for work that waits or computes",
        "concepts": ["WaitingThreadsOverlap", "GilBuildGivesNoSpeedup", "ProcessPoolSpeedsCpuWork", "FreeBuildScalesWithCores"],
        "also_from": ["IoBoundThreads", "CpuBoundThreads", "Processes", "PoolAndAsyncioMatch"],
        "read_from": "chapter 17 of the 2nd edition and the Python 3.14 documentation: threads suit work that waits, while work that computes needs processes or the free-threaded build",
        "why": "the passage is a sequence of steps with a test on whether the work waits or computes that leads to different tools: a workflow",
        "data": {
            "nodes": [
                {"id": "kind", "label": "Is the work waiting or computing?", "kind": "decision"},
                {"id": "wait", "label": "Threads, a pool or asyncio overlap the waiting"},
                {"id": "build", "label": "Is the free-threaded build running?", "kind": "decision"},
                {"id": "thr", "label": "Threads run in parallel on the free-threaded build"},
                {"id": "proc", "label": "A pool of processes computes in parallel"},
            ],
            "flows": [["start", "kind"], ["kind", "wait", "waits"], ["kind", "build", "computes"], ["build", "thr", "yes"], ["build", "proc", "no"], ["wait", "end"], ["thr", "end"], ["proc", "end"]],
        },
    },
    {
        "id": "TwoThreadsAndALock",
        "pattern": "Interaction",
        "title": "Two threads updating a shared counter with a lock",
        "concepts": ["ForcedLostUpdate", "LockFixesCounter", "IncrementIsSeveralSteps", "LockReleasedOnError"],
        "also_from": ["LostUpdates", "LocksAndEvents", "RaceInTheRecord"],
        "read_from": "chapter 17 and the threading documentation: threads that read and write the same variable trip over each other, and a lock makes the read and the write one step",
        "why": "the passage is an exchange between two threads and a lock in an order that matters - the lock is taken before the counter is read: an interaction",
        "data": {
            "participants": [
                {"id": "a", "label": "Thread A"},
                {"id": "lock", "label": "The lock"},
                {"id": "b", "label": "Thread B"},
            ],
            "messages": [
                ["a", "lock", "Acquires the lock"],
                ["a", "a", "Reads, adds one and writes the counter"],
                ["b", "lock", "Waits for the lock"],
                ["a", "lock", "Releases the lock"],
                ["lock", "b", "Lets thread B read the value", "reply"],
            ],
        },
    },
    {
        "id": "TheProducerAndTheConsumer",
        "pattern": "Interaction",
        "title": "A producer thread handing items to a consumer through a queue",
        "concepts": ["QueueHandsOver", "EventSignals", "SemaphoreLimits"],
        "also_from": ["LocksAndEvents", "LocalVariablesAreSafe"],
        "read_from": "the queue documentation and the producer-consumer problem: the producer puts items into the queue and the consumer takes them in order until the marker None",
        "why": "the passage is an exchange between a producer, a queue and a consumer in an order that matters - items are put before they are taken: an interaction",
        "data": {
            "participants": [
                {"id": "prod", "label": "The producer thread"},
                {"id": "q", "label": "The queue"},
                {"id": "cons", "label": "The consumer thread"},
            ],
            "messages": [
                ["prod", "q", "Puts the numbers into the queue"],
                ["prod", "q", "Puts the marker None into the queue"],
                ["cons", "q", "Takes the items in order"],
                ["q", "cons", "Hands over each item", "reply"],
                ["cons", "q", "Calls task_done() for each item"],
            ],
        },
    },
    {
        "id": "TheLifeOfAThread",
        "pattern": "LifeCycle",
        "title": "The life of a Thread object",
        "concepts": ["StartOnce", "JoinWaits", "ThreadNames", "DaemonDiesWithProgram"],
        "also_from": ["StartingThreads", "ThreadObjectsInfo", "DaemonThreads", "JoinBeforeStart"],
        "read_from": "chapter 17 and the threading documentation: a Thread object is created, started once, runs its target and is finished when the target returns",
        "why": "the passage follows one thread through the states it is in and names the call that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "new", "label": "The thread object is created"},
                {"id": "run", "label": "The thread is running its target"},
                {"id": "done", "label": "The thread has finished"},
            ],
            "initial": "new",
            "final": ["done"],
            "transitions": [
                ["new", "run", "start() runs the target in a new thread"],
                ["run", "done", "The target returns"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithThreads",
        "pattern": "SetOfUses",
        "title": "What a program can do with threads",
        "concepts": ["StartAThread", "ArgsAndKwargs", "JoinWaits", "LockFixesCounter", "QueueHandsOver", "MapKeepsOrder", "GatherOverlapsWaits"],
        "also_from": ["DaemonDiesWithProgram", "EventSignals", "FutureStates", "InterpreterPoolExists", "PopenReturnsAtOnce"],
        "read_from": "chapter 17 and the Python 3.14 documentation: start a thread, pass arguments, wait with join, guard data with a lock, hand items over with a queue, run a pool and overlap waiting with asyncio",
        "why": "the chapter and the documentation list independent things a program can ask the libraries to do - start, pass, wait, lock, queue, pool, await - a set of uses, not a sequence",
        "data": {
            "system": "THREADS",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "start", "label": "Start a thread with a target"},
                {"id": "args", "label": "Pass args and kwargs to the target"},
                {"id": "join", "label": "Wait for a thread with join()"},
                {"id": "lock", "label": "Guard a counter with a lock"},
                {"id": "queue", "label": "Hand items over with a queue"},
                {"id": "pool", "label": "Run functions on a pool with map()"},
                {"id": "aio", "label": "Overlap waiting with asyncio.gather()"},
            ],
            "links": [["prog", "start"], ["prog", "args"], ["prog", "join"], ["prog", "lock"], ["prog", "queue"], ["prog", "pool"], ["prog", "aio"]],
        },
    },
    {
        "id": "ThreadsAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Threads at a glance: seven branches",
        "concepts": ["ThreadBasics", "JoinAndDaemon", "SharedDataAndLocks", "ExecutorsAndPools", "GilAndFreeThreading", "ThreadsVersusOtherTools", "EnvironmentAndEvidence"],
        "also_from": ["StartingThreads", "ArgumentsOfThreads", "JoiningThreads", "DaemonThreads", "TheXkcdDownloader", "LostUpdates", "LocksAndEvents", "PoolBasics", "PoolErrors",
                      "InterpreterPools", "GilStatus", "CpuBoundThreads", "IoBoundThreads", "Processes", "AsyncioAndCoroutines", "Interpreters", "HonestyOfTheStudy",
                      "PrintedListingJoinFails", "FixedListingSkipsComics", "ForcedLostUpdate", "MapKeepsOrder", "GilOnInTheStandardBuild", "WaitingThreadsOverlap", "DefaultStartMethod",
                      "ProcessesDoNotShareVariables", "NotExecutedList", "SingleRunLabels", "RaceInTheRecord"],
        "read_from": "chapter 17 of the 2nd edition and the Python 3.14 documentation, the opening of each main subject: threads, join and daemon, shared data and locks, executors, the GIL, other tools and the evidence",
        "why": "the material classifies one topic, doing several things at once, by what each part is about and lists examples under each - a topic and its parts, with the one idea that holds for every part stated at the root",
        "data": {
            "root": "A program runs several threads at once",
            "branches": [
                {"label": "Thread basics",
                 "children": ["start() runs the target in a new thread", "args and kwargs pass the arguments", "The printed listing never starts its threads"]},
                {"label": "Join and daemon",
                 "children": ["join() waits for a thread", "A daemon thread dies with the program", "The downloader skips every tenth comic"]},
                {"label": "Shared data and locks",
                 "children": ["A lost update happens without a lock", "A lock makes the update one step", "A queue hands items over"]},
                {"label": "Executors and pools",
                 "children": ["map() keeps the order of the inputs", "An exception waits in the Future", "The default workers depend on the CPUs"]},
                {"label": "GIL and free threading",
                 "children": ["The standard build keeps the lock on", "Waiting threads overlap on both builds", "The free-threaded build scales with cores"]},
                {"label": "Threads versus other tools",
                 "children": ["A process does not share variables", "asyncio overlaps waiting on one thread", "The default start method is forkserver"]},
                {"label": "Environment and evidence",
                 "children": ["The study ran Python 3.14.6", "Every timing is a single run", "Windows and macOS were not executed"]},
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
    """the chapter's nodes read from the v1_0_0 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch25#"
    d = os.path.join(root, "03-materials", "ch25", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch25_document_v1_0_0.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch25_domain_abox_v1_0_0.ttl"))
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
