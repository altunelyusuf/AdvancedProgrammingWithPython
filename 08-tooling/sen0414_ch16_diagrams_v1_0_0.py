#!/usr/bin/env python3
"""SEN0414, chapter 16 (SQLite Databases, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
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
sen0414_ch15_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another
chapter is not edited); because chapter 16 has no page data yet, nodes_from_ttl() builds the node list from the chapter's RDODI
document and ABox, so the grounding can be measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch16_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "FromConnectToRows",
        "pattern": "Workflow",
        "title": "From connect() to the rows of a table and back to a closed file",
        "concepts": ["ConnectCreatesFile", "InsertColumnList", "FetchMethods", "CloseAndWarnings"],
        "also_from": ["Connecting", "Writing", "Reading", "SchemaIntrospection", "CreateIfNotExists", "BeginCommitRollback"],
        "read_from": "chapter 16, Creating Databases and Tables and CRUD Database Operations: connect to a file, create a table, "
                     "insert rows, commit, read the rows with execute and fetchall, and close the connection",
        "why": "the passage is the chapter's own sequence of steps, each depending on the one before it, with one choice "
               "after the statement runs, whether it changed the data: a workflow",
        "data": {
            "nodes": [
                {"id": "connect", "label": "Connect to a database file with connect()"},
                {"id": "table", "label": "Create the table if it does not exist"},
                {"id": "insert", "label": "Insert the rows with execute()"},
                {"id": "changed", "label": "Did the statement change the data?", "kind": "decision"},
                {"id": "commit", "label": "Commit the changes"},
                {"id": "read", "label": "Read the rows with fetchall()"},
                {"id": "close", "label": "Close the connection"},
            ],
            "flows": [["start", "connect"], ["connect", "table"], ["table", "insert"], ["insert", "changed"], ["changed", "commit", "yes"],
                      ["changed", "read", "no"], ["commit", "read"], ["read", "close"], ["close", "end"]],
        },
    },
    {
        "id": "ATransactionEnds",
        "pattern": "Workflow",
        "title": "A transaction: begin, change, then commit or roll back",
        "concepts": ["BeginCommitRollback", "AtomicStatement", "DurableAfterReopen", "AutocommitAttribute"],
        "also_from": ["Boundaries", "Guarantees", "ContextManagerTransaction", "LegacyAutocommit", "ConsistentConstraints", "TransactionControl"],
        "read_from": "chapter 16, Rolling Back Transactions: BEGIN starts a transaction, the statements change the data, commit() "
                     "keeps the changes and rollback() undoes them, and the ACID properties say what a failed statement leaves behind",
        "why": "the passage describes what happens to a group of changes step by step with one choice at the end, whether "
               "every statement succeeded, so that the changes are kept or undone: a workflow",
        "data": {
            "nodes": [
                {"id": "begin", "label": "Begin a transaction"},
                {"id": "change", "label": "Run the statements that change the data"},
                {"id": "ok", "label": "Did every statement succeed?", "kind": "decision"},
                {"id": "commit", "label": "Commit: the changes are kept"},
                {"id": "rollback", "label": "Roll back: the changes are undone"},
            ],
            "flows": [["start", "begin"], ["begin", "change"], ["change", "ok"], ["ok", "commit", "yes"], ["ok", "rollback", "no"],
                      ["commit", "end"], ["rollback", "end"]],
        },
    },
    {
        "id": "AParameterisedQuery",
        "pattern": "Interaction",
        "title": "A query with a placeholder against a query built by pasting text",
        "concepts": ["SqlInjection", "QmarkPlaceholders", "NamedPlaceholders"],
        "also_from": ["Parameters", "CrudOperations", "Reading", "FetchMethods"],
        "read_from": "chapter 16, Reading Data and the warning about SQL injection: the program sends the statement with a ? "
                     "placeholder and the value as a separate tuple, and SQLite treats the whole value as data",
        "why": "the passage is an exchange between the program, the module and SQLite in an order that matters - the statement "
               "and the value are sent apart, then the rows come back: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "mod", "label": "The sqlite3 module"},
                {"id": "db", "label": "SQLite"},
            ],
            "messages": [
                ["prog", "mod", "Calls execute() with a statement that has a placeholder"],
                ["prog", "mod", "Passes the value in a tuple"],
                ["mod", "db", "Sends the statement and binds the value as data"],
                ["db", "mod", "Returns the rows that match the name", "reply"],
                ["mod", "prog", "Returns a cursor to read the rows", "reply"],
            ],
        },
    },
    {
        "id": "ARowidThroughItsLife",
        "pattern": "LifeCycle",
        "title": "A rowid from the first insert to a reused number",
        "concepts": ["RowidReuse", "RowidAfterVacuum", "RowidHidden", "IntegerPrimaryKeyAlias"],
        "also_from": ["SpreadsheetVersusTable", "DatabaseIdea", "TableIsTupleList", "ForeignKeyMismatch"],
        "read_from": "chapter 16, Spreadsheets vs. Databases: SQLite adds a rowid column to each table, a unique integer that the "
                     "chapter says does not change when other rows are deleted; the SQLite pages qualify that claim",
        "why": "the passage follows one rowid through the states it can be in and names the event that moves it from each "
               "state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "none", "label": "No row yet"},
                {"id": "assigned", "label": "A row with a rowid"},
                {"id": "deleted", "label": "The row is deleted"},
                {"id": "reused", "label": "The rowid is handed out again"},
                {"id": "renumbered", "label": "The rowid changes after VACUUM"},
            ],
            "initial": "none",
            "final": [],
            "transitions": [
                ["none", "assigned", "An insert adds the row with the next rowid"],
                ["assigned", "deleted", "The delete statement deletes the row"],
                ["deleted", "reused", "A new insert reuses the rowid when it was the largest"],
                ["assigned", "renumbered", "VACUUM renumbers a table with no primary key"],
                ["reused", "assigned", "The new row holds the rowid"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithSqlite",
        "pattern": "SetOfUses",
        "title": "What a program can do with a SQLite database through sqlite3",
        "concepts": ["InsertColumnList", "UpdateDeleteWhere", "FetchMethods", "InnerJoin", "BackupMethod", "DumpMethod"],
        "also_from": ["Writing", "Reading", "Linking", "Changing", "Memory", "Dump", "CrudOperations", "TableStructure", "CopiesToolsAndPractice"],
        "read_from": "chapter 16: the module creates databases and tables, inserts, reads, updates and deletes rows, alters and "
                     "drops tables, joins tables with foreign keys, keeps a database in memory, backs it up and dumps it as text",
        "why": "the chapter lists independent things a program can do with the same database - write, read, change, join, "
               "copy, dump - a set of uses of the same module, not a sequence",
        "data": {
            "system": "A SQLITE DATABASE IN PYTHON",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "write", "label": "Insert rows into a table"},
                {"id": "read", "label": "Read rows with a query"},
                {"id": "change", "label": "Update and delete rows"},
                {"id": "alter", "label": "Alter and drop tables"},
                {"id": "join", "label": "Join tables with a foreign key"},
                {"id": "copy", "label": "Back up and dump a database"},
            ],
            "links": [["prog", "write"], ["prog", "read"], ["prog", "change"], ["prog", "alter"], ["prog", "join"], ["prog", "copy"]],
        },
    },
    {
        "id": "ChoosingHowToCopy",
        "pattern": "Workflow",
        "title": "Choosing how to copy a database",
        "concepts": ["BackupMethod", "DumpMethod", "InMemoryDatabase"],
        "also_from": ["Memory", "Dump", "DumpShippedFails", "CopiesToolsAndPractice", "SqliteCli"],
        "read_from": "chapter 16, Backing Up Databases, In-Memory Databases and Backups and Copying Databases: backup() copies a "
                     "database into another connection, iterdump() gives the SQL text of a database, and a memory database "
                     "can be copied to a file",
        "why": "the passage describes the steps of a copy and one choice, whether the copy should be a database or a text "
               "of SQL statements, with the step that follows each: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Connect to the database to copy"},
                {"id": "kind", "label": "Is the copy a database?", "kind": "decision"},
                {"id": "backup", "label": "Call backup() to copy into another connection"},
                {"id": "dump", "label": "Call iterdump() to get the SQL statements"},
                {"id": "check", "label": "Is there an error in the dump?", "kind": "decision"},
                {"id": "fix", "label": "Repair the foreign key and dump again"},
                {"id": "done", "label": "Finish with both connections"},
            ],
            "flows": [["start", "open"], ["open", "kind"], ["kind", "backup", "yes"], ["kind", "dump", "no"], ["backup", "done"],
                      ["dump", "check"], ["check", "fix", "yes"], ["check", "done", "no"], ["fix", "dump"], ["done", "end"]],
        },
    },
    {
        "id": "TwoWritersOneFile",
        "pattern": "Interaction",
        "title": "Two programs writing to one database file",
        "concepts": ["WriterLocked", "JournalModeWal"],
        "also_from": ["Concurrency", "TransactionControl", "IsolatedFromOthers", "DurableAfterReopen", "SqliteVersusServers"],
        "read_from": "chapter 16, SQLite vs. Other SQL Databases: SQLite is not the right choice for hundreds or thousands of "
                     "simultaneous write operations; this study ran 100 and 1,000 writers on one file",
        "why": "the passage is an exchange between two writers and the database file in an order that matters - one holds the "
               "lock, the other waits and tries again: an interaction",
        "data": {
            "participants": [
                {"id": "a", "label": "The first writer"},
                {"id": "b", "label": "The second writer"},
                {"id": "file", "label": "The database file"},
            ],
            "messages": [
                ["a", "file", "Begins a write and holds the lock"],
                ["b", "file", "Asks to write at the same time"],
                ["file", "b", "Answers that the database is locked", "reply"],
                ["a", "file", "Commits the transaction and releases the lock"],
                ["b", "file", "Writes after waiting for the lock"],
                ["file", "b", "Confirms the write", "reply"],
            ],
        },
    },
    {
        "id": "SqliteDatabasesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "SQLite databases at a glance: six branches",
        "concepts": ["DatabaseIdea", "ConnectionAndSchema", "CrudOperations", "TransactionControl", "TableStructure", "CopiesToolsAndPractice"],
        "also_from": ["SpreadsheetVersusTable", "SqliteVersusServers", "Connecting", "TypingRules", "Writing", "Parameters", "Reading",
                      "Speed", "Boundaries", "Guarantees", "Concurrency", "Changing", "Linking", "Memory", "Dump", "Tools", "Practice"],
        "read_from": "chapter 16, the opening of each of its main branches: the idea of a database, the connection and the schema, "
                     "the CRUD operations, transactions, the structure of tables and the copies, tools and practice programs",
        "why": "the chapter classifies one topic, working with SQLite from Python, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "SQLite: a database in one file that a program reads and writes with SQL",
            "branches": [
                {"label": "The idea of a database",
                 "children": ["A table is like a spreadsheet with a rowid",
                              "SQLite is one file with no server",
                              "A query replaces a loop over a list"]},
                {"label": "Connection and schema",
                 "children": ["connect() opens or creates the file",
                              "A STRICT table checks the types",
                              "The schema is read from sqlite_schema"]},
                {"label": "CRUD operations",
                 "children": ["Insert, update and delete change the rows",
                              "A placeholder keeps a value as data",
                              "An index speeds up a search"]},
                {"label": "Transactions",
                 "children": ["Commit keeps the changes and rollback undoes them",
                              "A failed statement changes nothing",
                              "Write-ahead logging helps several writers"]},
                {"label": "Table structure",
                 "children": ["Alter and drop change a table",
                              "A foreign key links two tables",
                              "A join reads them together"]},
                {"label": "Copies, tools and practice",
                 "children": ["backup() and iterdump() copy a database",
                              "The sqlite3 shell and three graphical apps",
                              "Two practice programs use the shipped file"]},
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
    """the chapter's nodes read from the v1_0_2 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch16#"
    d = os.path.join(root, "03-materials", "ch16", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch16_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch16_domain_abox_v1_0_2.ttl"))
    nodes = {}
    for s in g.subjects(DOC.sectionTitle, None):
        if not str(s).startswith(CHX + "S_"): continue
        cid = str(s)[len(CHX) + 2:]
        body = str(g.value(s, SKOS.definition) or "")
        nodes[cid] = {"id": cid, "label": str(g.value(s, RDFS.label)), "body": body.split("\n\n")[0], "definition": "", "parent": None, "_s": s}
    for cid, n in nodes.items():
        for p in g.subjects(DOC.hasSection, n["_s"]):
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
