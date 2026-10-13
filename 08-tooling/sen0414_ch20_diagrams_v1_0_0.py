#!/usr/bin/env python3
"""SEN0414, chapter 20 (Sending Email, Texts, and Push Notifications, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
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
sen0414_ch19_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another
chapter is not edited); because chapter 20 has no page data yet, nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_1
document and ABox, so the grounding can be measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch20_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "SendingAMailWithEzgmail",
        "pattern": "Workflow",
        "title": "Sending an email with EZGmail",
        "concepts": ["CredentialsAndToken", "ImportRunsInit", "SendCall", "AttachmentParts", "CcAndBccHeaders"],
        "also_from": ["GmailSetup", "GmailSending", "TokenFileContents", "GmailApi"],
        "read_from": "chapter 20, Enabling the API and Sending Mail: keep the credentials file and the token file in the working directory, call ezgmail.init() and, if no "
                     "error appears, call ezgmail.send() with the recipient, the subject and the body, a list of attachments and the keyword arguments cc and bcc",
        "why": "the passage is a numbered sequence of steps with one test, whether init() raises an error, that sends the reader back to the setup: a workflow",
        "data": {
            "nodes": [
                {"id": "files", "label": "Keep credentials.json and token.json in the working directory"},
                {"id": "init", "label": "Call ezgmail.init()"},
                {"id": "err", "label": "Does init() raise an error?", "kind": "decision"},
                {"id": "redo", "label": "Do the steps of the Google Cloud console again"},
                {"id": "send", "label": "Call ezgmail.send() with the recipient, the subject and the body"},
                {"id": "att", "label": "Pass a list of attachments"},
                {"id": "cc", "label": "Pass the keyword arguments cc and bcc"},
            ],
            "flows": [["start", "files"], ["files", "init"], ["init", "err"], ["err", "redo", "yes"], ["redo", "init"], ["err", "send", "no"],
                      ["send", "att"], ["att", "cc"], ["cc", "end"]],
        },
    },
    {
        "id": "ReadingMessagesFromANtfyTopic",
        "pattern": "Workflow",
        "title": "Receiving notifications from a ntfy topic by polling",
        "concepts": ["PollUrl", "JsonLines", "EventFields", "TopicSecrecy"],
        "also_from": ["NtfySubscribing", "NtfyPush", "NtfyServiceLimits", "DailyAndSize", "EmailControlLoop", "PracticePrograms"],
        "read_from": "chapter 20, Receiving Notifications: make a GET request for the topic URL that ends in /json?poll=1, split the text with splitlines(), parse "
                     "each line with json.loads() and read the message, and poll only once a minute or once every few minutes",
        "why": "the passage is a sequence of steps that repeats each time the program polls and has one test on the kind of event: a workflow",
        "data": {
            "nodes": [
                {"id": "get", "label": "Call requests.get() with the topic URL that ends in /json?poll=1"},
                {"id": "since", "label": "Add since to get the messages of the last minutes"},
                {"id": "split", "label": "Split the text of the answer into lines with splitlines()"},
                {"id": "parse", "label": "Parse each line with json.loads()"},
                {"id": "ev", "label": "Is the event a message?", "kind": "decision"},
                {"id": "read", "label": "Read the message, the title, the priority and the tags"},
                {"id": "wait", "label": "Wait a minute, then the program polls again"},
            ],
            "flows": [["start", "get"], ["get", "since"], ["since", "split"], ["split", "parse"], ["parse", "ev"], ["ev", "read", "yes"], ["ev", "wait", "no"],
                      ["read", "wait"], ["wait", "get"], ["wait", "end"]],
        },
    },
    {
        "id": "ControllingAComputerByEmail",
        "pattern": "Workflow",
        "title": "Email-Based Computer Control: one pass of the loop",
        "concepts": ["EmailControlLoop", "CommandInjectionRefused", "EnvelopeVersusHeader"],
        "also_from": ["PracticePrograms", "BookAndPractice", "ImapSession", "EmailTrust"],
        "read_from": "chapter 20, Email-Based Computer Control: check an email or ntfy account every 15 minutes, require a password in the message, launch the "
                     "program with subprocess.Popen(), wait for it, and delete the emails it handled",
        "why": "the passage walks through the steps of each check with a test on the password that sends the program back to wait: a workflow",
        "data": {
            "nodes": [
                {"id": "check", "label": "Check the mail for instructions"},
                {"id": "pw", "label": "Is the password in the message?", "kind": "decision"},
                {"id": "allow", "label": "Is the command on the allow-list?", "kind": "decision"},
                {"id": "run", "label": "Launch the program with Popen"},
                {"id": "wait", "label": "Wait for the program with wait()"},
                {"id": "del", "label": "Delete the emails the loop handled"},
                {"id": "sleep", "label": "Wait 15 minutes"},
            ],
            "flows": [["start", "check"], ["check", "pw"], ["pw", "allow", "yes"], ["pw", "del", "no"], ["allow", "run", "yes"], ["allow", "del", "no"],
                      ["run", "wait"], ["wait", "del"], ["del", "sleep"], ["sleep", "check"], ["sleep", "end"]],
        },
    },
    {
        "id": "PostingAPushNotification",
        "pattern": "Interaction",
        "title": "A program sending a push notification through ntfy",
        "concepts": ["PostBody", "MetadataHeaders", "ResponseObject", "PollUrl"],
        "also_from": ["NtfyPublishing", "NtfySubscribing", "NtfyPush", "TopicSecrecy"],
        "read_from": "chapter 20, Sending Notifications: requests.post() sends the text to the topic URL, anyone subscribed to the topic receives it "
                     "within a few seconds, and the program can poll the same topic with requests.get()",
        "why": "the passage is an exchange between the program, the service and a subscriber in an order that matters - the post comes before the poll: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "ntfy", "label": "The ntfy service"},
                {"id": "sub", "label": "A subscriber"},
            ],
            "messages": [
                ["prog", "ntfy", "Calls requests.post() with the topic URL and the text"],
                ["ntfy", "prog", "Returns a Response with the status 200", "reply"],
                ["sub", "ntfy", "Checks the topic for messages"],
                ["ntfy", "sub", "Returns the message of the topic", "reply"],
                ["prog", "ntfy", "Calls requests.get() with the topic URL and poll"],
                ["ntfy", "prog", "Returns one JSON object on each line", "reply"],
            ],
        },
    },
    {
        "id": "ASmtpSessionWithStarttls",
        "pattern": "Interaction",
        "title": "A program sending a message to an SMTP server with STARTTLS",
        "concepts": ["StarttlsSession", "LoginAfterTls", "EnvelopeRecipients", "RefusedRecipients"],
        "also_from": ["SmtpClient", "CertificateVerification", "StandardLibraryMail", "EnvelopeVersusHeader"],
        "read_from": "the smtplib documentation and the study's local SMTP server: the server advertises STARTTLS, the client upgrades the connection, logs in "
                     "and sends the message to the recipients of the envelope",
        "why": "the passage is an exchange between the client and the server in an order that matters - each command needs the answer of the one before: an interaction",
        "data": {
            "participants": [
                {"id": "client", "label": "The client program"},
                {"id": "server", "label": "The SMTP server"},
            ],
            "messages": [
                ["client", "server", "Calls ehlo() after connecting"],
                ["server", "client", "Advertises STARTTLS", "reply"],
                ["client", "server", "Calls starttls() with a context"],
                ["server", "client", "Answers 220 and the session uses TLS", "reply"],
                ["client", "server", "Calls login() with the user and the password"],
                ["server", "client", "Answers 235 Authentication successful", "reply"],
                ["client", "server", "Calls send_message() for the recipients"],
                ["server", "client", "Answers 250 for the message", "reply"],
            ],
        },
    },
    {
        "id": "AMessageInAnImapMailbox",
        "pattern": "LifeCycle",
        "title": "A message in an IMAP mailbox from arrival to expunge",
        "concepts": ["ImapSession", "ImapParsing", "EmailControlLoop"],
        "also_from": ["ImapClient", "StandardLibraryMail", "ImapIdle"],
        "read_from": "the imaplib documentation and the study's local IMAP server: a message arrives unseen, a fetch of RFC822 sets Seen, STORE marks it Deleted "
                     "and EXPUNGE removes it from the INBOX",
        "why": "the passage follows one message through the states it can be in and names the command that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "new", "label": "An unseen message in the INBOX"},
                {"id": "seen", "label": "A message with the Seen flag"},
                {"id": "marked", "label": "A message with the Deleted flag"},
                {"id": "gone", "label": "A message that EXPUNGE removed"},
            ],
            "initial": "new",
            "final": ["gone"],
            "transitions": [
                ["new", "new", "A fetch with BODY.PEEK leaves the message unseen"],
                ["new", "seen", "A fetch of RFC822 sets the Seen flag"],
                ["new", "marked", "STORE adds the Deleted flag"],
                ["seen", "marked", "STORE adds the Deleted flag"],
                ["marked", "gone", "EXPUNGE leaves the INBOX empty"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithEzgmail",
        "pattern": "SetOfUses",
        "title": "What a program can do with a Gmail account through EZGmail",
        "concepts": ["SendCall", "AttachmentParts", "UnreadRecentSearch", "ThreadVersusMessage", "AttachmentNames", "DownloadOverwrite", "ReplyThreading"],
        "also_from": ["GmailSending", "GmailReading", "GmailAttachments", "GmailApi", "MessageFields", "SummaryLine"],
        "read_from": "chapter 20, The Gmail API: send an email, attach files, list unread email, list recent email, search with the operators of the Gmail search box, "
                     "read the messages of a thread and download attachments",
        "why": "the chapter lists independent things a program can do with the same account - send, attach, list, search, read, download - "
               "a set of uses of the same module, not a sequence",
        "data": {
            "system": "THE GMAIL API THROUGH EZGMAIL",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "send", "label": "Send an email with ezgmail.send()"},
                {"id": "att", "label": "Attach files to an email"},
                {"id": "unread", "label": "List unread threads with unread()"},
                {"id": "search", "label": "Search with the operators of the Gmail search box"},
                {"id": "read", "label": "Read the messages of a thread"},
                {"id": "down", "label": "Download the attachments of a message"},
                {"id": "reply", "label": "Reply to a message in its thread"},
            ],
            "links": [["prog", "send"], ["prog", "att"], ["prog", "unread"], ["prog", "search"], ["prog", "read"], ["prog", "down"], ["prog", "reply"]],
        },
    },
    {
        "id": "SendingEmailTextsAndPushesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Sending email, texts and push notifications at a glance: six branches",
        "concepts": ["GmailApi", "StandardLibraryMail", "SmsGateways", "NtfyPush", "EmailTrust", "BookAndPractice"],
        "also_from": ["GmailSetup", "GmailSending", "GmailReading", "GmailAttachments", "MessageObjects", "SmtpClient", "ImapClient", "GmailByProtocol",
                      "GatewayAddressing", "GatewayRetreat", "SmsLimits", "NtfyPublishing", "NtfySubscribing", "NtfyServiceLimits", "EnvelopeAndHeaders",
                      "SenderAuthentication", "HeaderInjection", "ListingsAsPrinted", "PracticePrograms", "EditionChange", "TokenFileContents", "AttNotice",
                      "VerizonNotice", "Gsm7Length", "Ucs2Length", "TopicSecrecy", "DailyAndSize", "EnvelopeVersusHeader", "DmarcRecordParse", "SpfRecordParse",
                      "TestingModeExpiry", "FilenameTraversal", "ReplyThreading", "StarttlsSession", "CertificateVerification", "ImapIdle", "BodyEncoding",
                      "ResponseObject", "JsonLines", "NewlineInHeader", "CommandInjectionRefused", "ExampleDates", "UmbrellaReminder", "AutoUnsubscriber",
                      "MissingExampleImplementation", "SecondEditionContent", "DeprecatedOauthLibrary", "ListingsReplay"],
        "read_from": "chapter 20, the opening of each of its main branches: the Gmail API, the standard library, the SMS email gateways, ntfy, the trust in an "
                     "email, and the book and its practice programs",
        "why": "the chapter classifies one topic, reaching a person from a program, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "A program reaches a person by email, text or push notification",
            "branches": [
                {"label": "The Gmail API",
                 "children": ["The token file is a password",
                              "A reply keeps the thread id only",
                              "A name with a path is written outside"]},
                {"label": "The standard library",
                 "children": ["STARTTLS comes before the login",
                              "A Bcc recipient is in the envelope",
                              "IDLE is new in Python 3.14"]},
                {"label": "SMS email gateways",
                 "children": ["ATT ended its gateway in 2025",
                              "Verizon ends its gateway in 2027",
                              "160 characters in GSM-7, 70 in UCS-2"]},
                {"label": "ntfy",
                 "children": ["The topic name is the password",
                              "The limit is 4096 bytes",
                              "The answer is one JSON object on each line"]},
                {"label": "Trust in an email",
                 "children": ["The envelope and the From header differ",
                              "A line break in a header is refused",
                              "A command in a subject needs an allow-list"]},
                {"label": "The book and practice",
                 "children": ["The online materials hold no file",
                              "The 2nd edition taught smtplib",
                              "The forecast has a chance of precipitation"]},
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
    CHX = "http://example.org/sen0414/ch20#"
    d = os.path.join(root, "03-materials", "ch20", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch20_document_v1_0_1.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch20_domain_abox_v1_0_1.ttl"))
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
