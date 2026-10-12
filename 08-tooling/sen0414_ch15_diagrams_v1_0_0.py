#!/usr/bin/env python3
"""SEN0414, chapter 15 (Google Sheets, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case
diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts
whose explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects. Every element label is made of words that occur in the first paragraph
and the definition of the accompanying concepts or their section, which is the text the page shows; run_checks() measures
that (the grounding ratio, required here to be 0.84 or more, where the shared rule of the earlier chapters asks 0.8)
besides the structural rules. This module follows the layout of sen0414_ch14_diagrams_v1_0_0.py (the helper functions
below are the same rules, written again because a file of another chapter is not edited); because chapter 15 has no page
data yet, nodes_from_ttl() builds the node list from the chapter's RDODI document and ABox, so the grounding can be
measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch15_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "FromCredentialsToSignedIn",
        "pattern": "Workflow",
        "title": "From a Google Cloud project to a script that is signed in",
        "concepts": ["CloudProjectIds", "ApiEnablement", "ConsentScreenUi", "CredentialsFile", "TokenFiles", "LocalServerFlow"],
        "also_from": ["GoogleAccess", "CloudProject", "ConsentScreen", "CredentialFiles", "SignInFlow", "TokenLifetime", "ScopesChosen", "TestUsers"],
        "read_from": "chapter 15, Installing and Setting Up EZSheets: create a Google Cloud project, switch on the Sheets and Drive "
                     "APIs, configure the OAuth consent screen, create and download the credentials file, and at the first run let "
                     "the library open the browser so that it writes the token files",
        "why": "the passage is the chapter's own sequence of setup steps, each depending on the one before it, with one choice "
               "at the end, whether the token files exist and are valid: a workflow",
        "data": {
            "nodes": [
                {"id": "project", "label": "Create a Google Cloud project with a project ID"},
                {"id": "apis", "label": "Switch on the Sheets API and the Drive API"},
                {"id": "consent", "label": "Set the consent screen and the scopes"},
                {"id": "creds", "label": "Download the credentials file into the folder"},
                {"id": "tokens", "label": "Are the token files valid?", "kind": "decision"},
                {"id": "browser", "label": "The browser opens the consent page"},
                {"id": "write", "label": "The library writes the token files"},
                {"id": "ready", "label": "Open a spreadsheet"},
            ],
            "flows": [["start", "project"], ["project", "apis"], ["apis", "consent"], ["consent", "creds"], ["creds", "tokens"],
                      ["tokens", "ready", "yes"], ["tokens", "browser", "no"], ["browser", "write"], ["write", "ready"], ["ready", "end"]],
        },
    },
    {
        "id": "ProjectElevenAudit",
        "pattern": "Workflow",
        "title": "Project 11, Step 1: auditing the fake blockchain, row by row",
        "concepts": ["AuditProgram", "GetRowColumn", "BlankRowError"],
        "also_from": ["BlockchainLedger", "LedgerProjects", "TransactionProgram", "UpdateAllRows", "RowsColumns"],
        "read_from": "chapter 15, Step 1: open the Boringcoin sheet, loop over every row for the sender, the recipient and the "
                     "amount, create money for the sender PRE-MINE, move funds from the sender to the recipient otherwise, then "
                     "print the dictionary and add up the total",
        "why": "the passage describes what the program does step by step and in a loop, with one choice on the way, whether the "
               "sender is PRE-MINE: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Open the Boringcoin sheet and get its rows"},
                {"id": "row", "label": "Read the sender, the recipient and the amount of each row"},
                {"id": "pre", "label": "Is the sender PRE-MINE?", "kind": "decision"},
                {"id": "mint", "label": "Add the amount to the recipient from nothing"},
                {"id": "move", "label": "Take the amount from the sender and add it to the recipient"},
                {"id": "more", "label": "Are more rows to read in the sheet?", "kind": "decision"},
                {"id": "print", "label": "Print the dictionary of balances"},
                {"id": "total", "label": "Add up the total of the balances"},
            ],
            "flows": [["start", "open"], ["open", "row"], ["row", "pre"], ["pre", "mint", "yes"], ["pre", "move", "no"], ["mint", "more"],
                      ["move", "more"], ["more", "row", "yes"], ["more", "print", "no"], ["print", "total"], ["total", "end"]],
        },
    },
    {
        "id": "ProjectElevenTransaction",
        "pattern": "Workflow",
        "title": "Project 11, Step 2: adding a transaction from the command line",
        "concepts": ["TransactionProgram", "ArgvUnpacking", "RequestsPerCall", "AppendRace"],
        "also_from": ["BlockchainLedger", "LedgerProjects", "RequestCost", "RequestPerWrite", "CellByColumnRow", "SheetSize"],
        "read_from": "chapter 15, Step 2: get the sender, the recipient and the amount from the command line arguments, open the "
                     "sheet, add one to rowCount and write the three values into the new row",
        "why": "the passage lists what the program does in order, with one choice on the way, whether the command line holds "
               "enough arguments, and ends by writing the new row: a workflow",
        "data": {
            "nodes": [
                {"id": "args", "label": "Does the number of command line arguments reach three?", "kind": "decision"},
                {"id": "usage", "label": "Print a line and end the program"},
                {"id": "unpack", "label": "Unpack the sender, the recipient and the amount"},
                {"id": "open", "label": "Open the sheet of the Boringcoin spreadsheet"},
                {"id": "count", "label": "Add one to rowCount, which costs three requests"},
                {"id": "write", "label": "Write the three values into the new row"},
            ],
            "flows": [["start", "args"], ["args", "usage", "no"], ["usage", "end"], ["args", "unpack", "yes"], ["unpack", "open"],
                      ["open", "count"], ["count", "write"], ["write", "end"]],
        },
    },
    {
        "id": "AWriteAndARead",
        "pattern": "Interaction",
        "title": "A cell written by the program and read back from the local copy",
        "concepts": ["ValuesAsText", "RequestPerWrite", "RefreshMethod", "CellByAddress"],
        "also_from": ["CellAccess", "RequestCost", "SpreadsheetAttributes", "EmptyCell", "RangeNotation", "SheetObjects"],
        "read_from": "chapter 15, Reading and Writing Data: assigning to a cell sends a write request, reading it returns what the "
                     "sheet holds, and refresh() reads the spreadsheet again; the chapter prints the value 30 as a string",
        "why": "the passage is an exchange between the program, the library and Google in an order that matters - the value is "
               "written, read back, and read again after a refresh: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "lib", "label": "The Sheet object of the library"},
                {"id": "google", "label": "Google Sheets"},
            ],
            "messages": [
                ["prog", "lib", "Assigns 30 to the cell B2"],
                ["lib", "google", "Sends one write request with USER_ENTERED"],
                ["google", "lib", "Answers that the write is done", "reply"],
                ["prog", "lib", "Reads the cell B2"],
                ["lib", "prog", "Returns the value written, 30, from the local copy", "reply"],
                ["prog", "lib", "Calls refresh() to read the sheet again"],
                ["lib", "google", "Reads the values of the sheet"],
                ["google", "lib", "Returns the value as text, 30", "reply"],
            ],
        },
    },
    {
        "id": "ATokenFile",
        "pattern": "LifeCycle",
        "title": "A token file from the first sign-in to a refused refresh",
        "concepts": ["TokenLifetime", "TokenFiles", "LocalServerFlow", "TokenPickle"],
        "also_from": ["ConsentScreen", "CredentialFiles", "SignInFlow", "TestUsers", "NoBrowserFailure", "GoogleAccess"],
        "read_from": "chapter 15, Logging In with the Credentials File: the library opens the browser, writes the token files "
                     "once, and does not ask again; Google's pages add that a refresh token of a testing app expires in seven days",
        "why": "the passage follows one token file through the states it can be in and names the event that moves it from each "
               "state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "none", "label": "No token file"},
                {"id": "valid", "label": "A valid token file"},
                {"id": "expired", "label": "An expired token"},
                {"id": "refused", "label": "A stale token file"},
            ],
            "initial": "none",
            "final": [],
            "transitions": [
                ["none", "valid", "The sign-in in the browser writes the token files"],
                ["valid", "expired", "The access token expires"],
                ["expired", "valid", "The refresh token gets a new access token"],
                ["expired", "refused", "Google refuses the refresh after seven days"],
                ["refused", "none", "The reader deletes the token files"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithEzsheets",
        "pattern": "SetOfUses",
        "title": "What a program can do with a Google account through EZSheets",
        "concepts": ["NewSpreadsheet", "UploadSpreadsheet", "DownloadFormats", "TrashAndDelete", "GetRowColumn", "CopySheet"],
        "also_from": ["SpreadsheetObjects", "OpeningSpreadsheets", "FileTransfer", "ListingDeleting", "SheetObjects", "RowsColumns",
                      "SheetLifecycle", "ListSpreadsheets", "SheetIndex", "UpdateAllRows"],
        "read_from": "chapter 15: the library creates, uploads, lists and deletes spreadsheets, downloads them as Excel, "
                     "OpenOffice, CSV, TSV, PDF or HTML, reads and writes cells, rows and columns, and creates, moves, deletes "
                     "and copies sheets",
        "why": "the chapter lists independent things a program can do with the same account - create, upload, download, delete, "
               "read, write, copy - a set of uses of the same library, not a sequence",
        "data": {
            "system": "A GOOGLE ACCOUNT IN EZSHEETS",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "create", "label": "Create or upload spreadsheets"},
                {"id": "list", "label": "List spreadsheets and delete them"},
                {"id": "down", "label": "Download spreadsheets in six formats"},
                {"id": "cells", "label": "Read and write cells, rows and columns"},
                {"id": "sheets", "label": "Create, move and delete sheets"},
                {"id": "copy", "label": "Copy a sheet to another spreadsheet"},
            ],
            "links": [["prog", "create"], ["prog", "list"], ["prog", "down"], ["prog", "cells"], ["prog", "sheets"], ["prog", "copy"]],
        },
    },
    {
        "id": "AQuotaRetry",
        "pattern": "Workflow",
        "title": "A request that meets the quota: the throttle and the retry",
        "concepts": ["RetryOnQuota", "LibraryThrottle", "IgnoreQuotaFlag", "GoogleQuotas"],
        "also_from": ["QuotaRules", "RequestsAndQuotas", "RequestCost", "BatchedUpdate", "PayloadSize"],
        "read_from": "chapter 15, Working with Google Sheets Quotas: the library catches the quota exception and retries the "
                     "request, so calls may take several seconds, and re-raises the exception if the request keeps failing",
        "why": "the passage describes what the library does with one request, step by step and in a loop with two choices, "
               "whether Google refuses it and whether the tries are used up: a workflow",
        "data": {
            "nodes": [
                {"id": "throttle", "label": "The library sleeps while too many writes are in a burst"},
                {"id": "send", "label": "Send the request to Google"},
                {"id": "refused", "label": "Does Google answer RESOURCE_EXHAUSTED?", "kind": "decision"},
                {"id": "left", "label": "Is the limit of tries exhausted?", "kind": "decision"},
                {"id": "pause", "label": "Pause for several seconds and retry"},
                {"id": "raise", "label": "Raise the exception to the program"},
                {"id": "done", "label": "Return the answer"},
            ],
            "flows": [["start", "throttle"], ["throttle", "send"], ["send", "refused"], ["refused", "done", "no"], ["refused", "left", "yes"],
                      ["left", "raise", "yes"], ["left", "pause", "no"], ["pause", "send"], ["done", "end"], ["raise", "end"]],
        },
    },
    {
        "id": "GoogleSheetsAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Google Sheets at a glance: six branches",
        "concepts": ["GoogleAccess", "SpreadsheetObjects", "SheetObjects", "RequestsAndQuotas", "LedgerProjects", "LibraryContext"],
        "also_from": ["CloudProject", "ConsentScreen", "CredentialFiles", "SignInFlow", "OpeningSpreadsheets", "FileTransfer", "CellAccess",
                      "RowsColumns", "SheetLifecycle", "RequestCost", "QuotaRules", "BlockchainLedger", "PracticePrograms",
                      "LibraryStatus", "GoogleClients", "InterpreterRuns"],
        "read_from": "chapter 15, the opening of each of its main branches: the setup of access, spreadsheet objects, sheet "
                     "objects, quotas, the Boringcoin project and the practice programs, and the library behind them",
        "why": "the chapter classifies one topic, working with Google Sheets from Python, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "Google Sheets: a program reads and writes spreadsheets by web requests",
            "branches": [
                {"label": "Access to a Google account",
                 "children": ["A Cloud project, the two APIs and a consent screen",
                              "A credentials file and two token files",
                              "The first sign-in opens a browser"]},
                {"label": "Spreadsheet objects",
                 "children": ["A spreadsheet is opened by URL, id or title",
                              "It is uploaded and downloaded in six formats",
                              "Deleting sends it to the Trash"]},
                {"label": "Sheet objects",
                 "children": ["A cell is got by address or by column and row",
                              "Rows and columns are read and written as lists",
                              "Sheets are created, moved, deleted and copied"]},
                {"label": "Requests and quotas",
                 "children": ["Every write is one request",
                              "Google limits the requests per minute",
                              "The library throttles and retries"]},
                {"label": "The Boringcoin project",
                 "children": ["The audit adds up the balances of the accounts",
                              "The transaction program adds a row",
                              "The practice programs read forms and check totals"]},
                {"label": "The library and Google's clients",
                 "children": ["EZSheets is built on the Google client libraries",
                              "Its documentation is dated November 2019",
                              "The same program runs under every 3.14 release"]},
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
    """the chapter's nodes read from the v1_0_1 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch15#"
    d = os.path.join(root, "03-materials", "ch15", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch15_document_v1_0_1.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch15_domain_abox_v1_0_1.ttl"))
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
