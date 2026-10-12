#!/usr/bin/env python3
"""SEN0414, chapter 13 (Web Scraping, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
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
besides the structural rules. This module follows the layout of sen0414_ch12_diagrams_v1_0_1.py (the helper functions
below are the same rules, written again because a file of another chapter is not edited); because chapter 13 has no page
data yet, nodes_from_ttl() builds the node list from the chapter's RDODI document and ABox, so the grounding can be
measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch13_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "ChoosingTheTool",
        "pattern": "Workflow",
        "title": "Which tool reaches the page in front of the program",
        "concepts": ["DynamicPages", "WebbrowserOpen", "SoupObject", "ServiceEndpoint", "ToolChoice"],
        "also_from": ["Fetching", "Services", "Parsing", "Browsers", "GetRequest", "JsonDecoding", "HeadlessMode"],
        "read_from": "chapter 13, its opening list of modules and the section on Selenium: webbrowser opens a page for the "
                     "user, requests downloads it, an API is preferred when the service offers one, Beautiful Soup reads "
                     "downloaded HTML, and Selenium or Playwright is needed when the page depends on JavaScript or a login",
        "why": "the passage helps a reader decide between five tools by asking questions about the page in turn - should "
               "the user see it, does a service offer an API, is the data already in the HTML - and each answer leads to a "
               "different tool: a workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "page", "label": "A page or a service the program needs"},
                {"id": "see", "label": "Should the user see the page in a browser?", "kind": "decision"},
                {"id": "open", "label": "webbrowser.open() launches the user's browser"},
                {"id": "api", "label": "Does the service offer an API?", "kind": "decision"},
                {"id": "json", "label": "requests.get() on the endpoint, then json.loads()"},
                {"id": "static", "label": "Is the data in the HTML that requests downloads?", "kind": "decision"},
                {"id": "soup", "label": "BeautifulSoup parses the text; select() finds the elements"},
                {"id": "drive", "label": "Selenium or Playwright drives a real browser"},
            ],
            "flows": [["start", "page"], ["page", "see"], ["see", "open", "yes"], ["see", "api", "no"], ["api", "json", "yes"],
                      ["api", "static", "no"], ["static", "soup", "yes"], ["static", "drive", "no, a script builds it"],
                      ["open", "end"], ["json", "end"], ["soup", "end"], ["drive", "end"]],
        },
    },
    {
        "id": "ThePoliteCrawl",
        "pattern": "Workflow",
        "title": "A crawler that reads robots.txt before it fetches",
        "concepts": ["RobotsTxt", "PoliteDelay", "PoliteCrawler"],
        "also_from": ["CrawlerManners", "ComicCrawler", "ComicProgram"],
        "read_from": "chapter 13, the comic downloader's limit of ten downloads and its one-second sleep, with RFC 9309 and "
                     "urllib.robotparser: a crawler reads robots.txt first, asks can_fetch for each path, skips what the "
                     "file disallows and waits the Crawl-delay between pages",
        "why": "the passage describes what a polite crawler does, step by step and in a loop, with one choice on the "
               "way, whether the path may be fetched: a workflow",
        "data": {
            "nodes": [
                {"id": "read", "label": "Read the robots.txt of the site first"},
                {"id": "next", "label": "Pick a path of the crawl"},
                {"id": "may", "label": "Does can_fetch allow the path?", "kind": "decision"},
                {"id": "skip", "label": "Skip the path the file disallows"},
                {"id": "get", "label": "Download the page and follow its links"},
                {"id": "wait", "label": "Wait the Crawl-delay between pages"},
                {"id": "more", "label": "Is a path left, and is the limit of downloads unmet?", "kind": "decision"},
            ],
            "flows": [["start", "read"], ["read", "next"], ["next", "may"], ["may", "get", "yes"], ["may", "skip", "no"],
                      ["get", "wait"], ["wait", "more"], ["skip", "more"], ["more", "next", "yes"], ["more", "end", "no"]],
        },
    },
    {
        "id": "ACheckedDownload",
        "pattern": "Workflow",
        "title": "Downloading a file and saving it, with the checks",
        "concepts": ["GetRequest", "RequestTimeout", "RaiseForStatus", "BinaryWrite", "ChunkedDownload"],
        "also_from": ["PageDownload", "ResponseChecking", "FileSaving", "StatusCheck"],
        "read_from": "chapter 13, the review of file downloading and saving: call requests.get(), call raise_for_status(), "
                     "open the file with 'wb', loop over iter_content() and write each chunk; the requests documentation "
                     "adds a timeout and stream=True",
        "why": "the passage is the chapter's own list of steps for one download, in order, with one point where the "
               "program stops, a bad status: a workflow",
        "data": {
            "nodes": [
                {"id": "get", "label": "requests.get() the URL, with a timeout"},
                {"id": "ok", "label": "Did raise_for_status() raise an exception?", "kind": "decision"},
                {"id": "stop", "label": "The program stops, or the exception is caught and printed"},
                {"id": "open", "label": "Open the file in write binary mode with 'wb'"},
                {"id": "loop", "label": "Loop over iter_content() and write each chunk"},
                {"id": "done", "label": "The file holds the bytes; write() returned their number"},
            ],
            "flows": [["start", "get"], ["get", "ok"], ["ok", "stop", "yes"], ["ok", "open", "no"], ["open", "loop"],
                      ["loop", "done"], ["stop", "end"], ["done", "end"]],
        },
    },
    {
        "id": "AWeatherCall",
        "pattern": "Interaction",
        "title": "Two calls to the weather API, one answer feeding the next",
        "concepts": ["ServiceEndpoint", "AccessKey", "JsonDecoding", "UnitConversion"],
        "also_from": ["ApiCalls", "ApiData", "ErrorAnswer"],
        "read_from": "chapter 13, accessing a weather API: the program asks the geocoding endpoint for the latitude and "
                     "longitude of San Francisco, decodes the JSON, asks the weather endpoint with them and converts the "
                     "temperature from Kelvin",
        "why": "the passage is an exchange between the program and a service in an order that matters - the first answer "
               "is the input of the second request - an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "api", "label": "The OpenWeather service"},
            ],
            "messages": [
                ["prog", "api", "GET /geo/1.0/direct?q=San Francisco,CA,US&appid=API key"],
                ["api", "prog", "a JSON list; item 0 has lat and lon", "reply"],
                ["prog", "prog", "json.loads() decodes the text into lists and dictionaries"],
                ["prog", "api", "GET /data/2.5/weather?lat=...&lon=...&appid=API key"],
                ["api", "prog", "a JSON dictionary; main temp is in Kelvin", "reply"],
                ["prog", "prog", "round(285.44 - 273.15, 1) converts to Celsius"],
            ],
        },
    },
    {
        "id": "ACheckboxInPlaywright",
        "pattern": "LifeCycle",
        "title": "A checkbox's state under click, check and uncheck",
        "concepts": ["CheckBoxes", "FillAndPress"],
        "also_from": ["PlaywrightElements", "LocatorMethods", "PageLocators"],
        "read_from": "chapter 13, clicking elements with Playwright: click() toggles a checkbox to the opposite state, "
                     "check() and uncheck() leave it checked or unchecked whatever it was, and set_checked() takes True or "
                     "False",
        "why": "the passage follows one checkbox through the states it can be in and names the call that moves it from "
               "each state to the next, one that depends on the state and two that do not: a life cycle",
        "data": {
            "states": [
                {"id": "unchecked", "label": "Unchecked"},
                {"id": "checked", "label": "Checked"},
            ],
            "initial": "unchecked",
            "final": [],
            "transitions": [
                ["unchecked", "checked", "click() toggles it to the opposite state"],
                ["checked", "unchecked", "click() toggles it to the opposite state"],
                ["unchecked", "checked", "check() or set_checked(True)"],
                ["checked", "unchecked", "uncheck() or set_checked(False)"],
                ["checked", "checked", "check() leaves it checked"],
                ["unchecked", "unchecked", "uncheck() leaves it unchecked"],
            ],
        },
    },
    {
        "id": "AMistypedSelector",
        "pattern": "Interaction",
        "title": "What happens when Playwright is given a mistyped selector",
        "concepts": ["AutoWaiting", "LocatorMethods"],
        "also_from": ["PlaywrightElements", "ElementLookup", "PageLocators"],
        "read_from": "chapter 13, finding elements with Playwright: a locator stands for elements that may exist later, "
                     "so Playwright waits 30 seconds for an element that does not exist, while is_visible() and "
                     "query_selector() answer at once",
        "why": "the passage is an exchange between the program and the page in an order that matters - a request, a wait, "
               "a failure, and a quick check that answers at once - an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "pw", "label": "Playwright and the page"},
            ],
            "messages": [
                ["prog", "pw", "page.locator() with a selector for an element, then click()"],
                ["pw", "pw", "waits for the element, up to a default timeout of 30 seconds"],
                ["pw", "prog", "A timeout after 30 seconds", "reply"],
                ["prog", "pw", "is_visible() or query_selector() with the selector"],
                ["pw", "prog", "An answer at once: not visible, or no element", "reply"],
            ],
        },
    },
    {
        "id": "WhatASeleniumProgramDoes",
        "pattern": "SetOfUses",
        "title": "What a Selenium program can do with the elements of a page",
        "concepts": ["ByLocators", "ElementLookup", "ElementProperties", "ClickAndSubmit", "SpecialKeys"],
        "also_from": ["SeleniumElements", "BrowserButtons", "WebDriverStart"],
        "read_from": "chapter 13, controlling the browser with Selenium: find elements with find_element() and By constants, "
                     "read their text and attributes, click them, type into fields and submit forms, and send keys such as "
                     "Keys.END",
        "why": "the passage lists independent things a program can do with the page's elements - find, read, click, type, "
               "scroll - a set of uses of the same driver, not a sequence",
        "data": {
            "system": "A BROWSER STARTED BY SELENIUM",
            "actors": [{"id": "prog", "label": "A Selenium program"}],
            "usecases": [
                {"id": "find", "label": "Find elements with find_element() and a By constant"},
                {"id": "read", "label": "Read an element's text, attributes and properties"},
                {"id": "click", "label": "Click a link or a button with click()"},
                {"id": "type", "label": "Type into a field with send_keys(); submit() the form"},
                {"id": "keys", "label": "Scroll with the Keys constants, such as Keys.END"},
            ],
            "links": [["prog", "find"], ["prog", "read"], ["prog", "click"], ["prog", "type"], ["prog", "keys"]],
        },
    },
    {
        "id": "WebScrapingAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Web scraping at a glance: six branches",
        "concepts": ["Protocol", "Fetching", "Services", "Parsing", "Programs", "Browsers"],
        "also_from": ["AddressForms", "ProtocolBasics", "CrawlerManners", "BrowserOpening", "PageDownload", "ApiCalls",
                      "ApiData", "MarkupBasics", "SoupObjects", "SearchProgram", "ComicProgram", "SeleniumDriver",
                      "PlaywrightDriver", "ToolChoice"],
        "read_from": "chapter 13, the opening of each of its main branches: the address and the protocol, fetching a page "
                     "with webbrowser and requests, a weather API, HTML and Beautiful Soup, the three projects and the "
                     "practice programs, and driving a browser with Selenium and Playwright",
        "why": "the chapter classifies one topic, getting data from the web, by what each branch is about and lists "
               "examples under each - a topic and its parts, laid out to remember, with the one idea that holds for every "
               "part stated once at the root",
        "data": {
            "root": "Web scraping: a program uses the web",
            "branches": [
                {"label": "Protocol: the address and the manners",
                 "children": ["A URL has a scheme, a host, a path, a query and a fragment",
                              "A status code begins every answer",
                              "A robots.txt file asks crawlers to keep away"]},
                {"label": "Fetching a page",
                 "children": ["webbrowser.open() shows a URL in the user's browser",
                              "requests.get() downloads a page into the program",
                              "raise_for_status() stops the program on a bad download"]},
                {"label": "Web services and their APIs",
                 "children": ["An endpoint is the URL of one request",
                              "An API key identifies the account",
                              "json.loads() decodes the answer"]},
                {"label": "Parsing HTML",
                 "children": ["An element is a tag, its content and a closing tag",
                              "The Developer Tools show the HTML of a page",
                              "select() takes a CSS selector and returns Tag objects"]},
                {"label": "Programs of the chapter",
                 "children": ["searchpypi.py opens the first search results",
                              "downloadXkcdComics.py follows the Prev link",
                              "Link verification tests every link for 404"]},
                {"label": "Driving a browser",
                 "children": ["Selenium starts Firefox with webdriver.Firefox()",
                              "Playwright runs headless by default",
                              "A driven browser is needed when a script builds the page"]},
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
    CHX = "http://example.org/sen0414/ch13#"
    d = os.path.join(root, "03-materials", "ch13", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch13_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch13_domain_abox_v1_0_2.ttl"))
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
