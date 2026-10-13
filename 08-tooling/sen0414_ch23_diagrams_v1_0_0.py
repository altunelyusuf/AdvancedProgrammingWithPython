#!/usr/bin/env python3
"""SEN0414, chapter 23 (Controlling the Keyboard and Mouse, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of a thing a state
diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram type lives in
the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts
whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations
the content draws on), one sentence saying why the pattern fits, and the diagram's content in the element names the renderer of that type expects. Every
element label is made of words that occur in the first paragraph and the definition of the accompanying concepts or their section, which is the text the page
shows; run_checks() measures that (the grounding ratio, required here to be 0.84 or more) besides the structural rules. This module follows the layout of
sen0414_ch22_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another chapter is not edited); nodes_from_ttl()
builds the node list from the chapter's RDODI v1_0_2 document and ABox, so the grounding is measured on the section's first paragraph, which is what the page
uses as the body.

Usage: python3 sen0414_ch23_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "ACallWithTheFailSafeOn",
        "pattern": "Workflow",
        "title": "What happens when a script calls a PyAutoGUI function with the fail-safe on",
        "concepts": ["PauseDefault", "FailsafeCorners", "FailsafeFires", "FailsafeSlam"],
        "also_from": ["FailsafePointsFixed", "PausesAndFailSafes", "StayingOnTrack"],
        "read_from": "chapter 23, Pauses and Fail-Safes: after a function call PyAutoGUI waits one tenth of a second, and if the cursor is in a corner it raises "
                     "the exception that stops the program",
        "why": "the passage is a sequence of steps with one test on whether the cursor is in a corner that sends the program on or stops it: a workflow",
        "data": {
            "nodes": [
                {"id": "call", "label": "The script calls a PyAutoGUI function"},
                {"id": "pause", "label": "PyAutoGUI waits for the pause after the call"},
                {"id": "corner", "label": "Is the cursor in a corner of the screen?", "kind": "decision"},
                {"id": "raise", "label": "PyAutoGUI raises the exception and the program stops"},
                {"id": "next", "label": "The program goes on to the next function call"},
            ],
            "flows": [["start", "call"], ["call", "pause"], ["pause", "corner"], ["corner", "raise", "yes"], ["corner", "next", "no"], ["raise", "end"], ["next", "end"]],
        },
    },
    {
        "id": "FindingAndClickingAButton",
        "pattern": "Workflow",
        "title": "Finding a button in a screenshot and clicking it",
        "concepts": ["ScreenshotImage", "LocateBox", "LocateAllAndClick", "ImageNotFound", "LocateWaits"],
        "also_from": ["ImageRecognition", "ExactMatchAndConfidence", "ScalingMismatch", "ScreenshotNeedsScrot"],
        "read_from": "chapter 23, Image Recognition: locateOnScreen() looks for the picture of a button in a screenshot and returns its box, or raises "
                     "ImageNotFoundException when the image cannot be found",
        "why": "the passage is a sequence of steps with a test on whether the image was found that leads to a click or to an exception: a workflow",
        "data": {
            "nodes": [
                {"id": "shot", "label": "Take a screenshot of the screen"},
                {"id": "loc", "label": "Call locateOnScreen() with the image of the button"},
                {"id": "found", "label": "Is the image found?", "kind": "decision"},
                {"id": "click", "label": "Click the center of the box"},
                {"id": "exc", "label": "The call raises ImageNotFoundException"},
            ],
            "flows": [["start", "shot"], ["shot", "loc"], ["loc", "found"], ["found", "click", "yes"], ["found", "exc", "no"], ["click", "end"], ["exc", "end"]],
        },
    },
    {
        "id": "TypingIntoTheRightWindow",
        "pattern": "Workflow",
        "title": "Typing a string into a window that has the focus",
        "concepts": ["FocusDecides", "WriteString", "HotkeyOrder", "SleepAndCountdown"],
        "also_from": ["WriteInterval", "HoldContext", "HotkeysAndFocus", "TypingText"],
        "read_from": "chapter 23, Sending Keystrokes: click to make the window active, call write() to type the string and hotkey() to press a shortcut, because "
                     "the focused window receives the typing",
        "why": "the passage is a sequence of steps in which each step depends on the window the one before it made active: a workflow",
        "data": {
            "nodes": [
                {"id": "wait", "label": "Wait a few seconds with sleep()"},
                {"id": "click", "label": "Click the window to make it active"},
                {"id": "write", "label": "Call write() to type the string"},
                {"id": "hot", "label": "Call hotkey() to press the shortcut"},
                {"id": "recv", "label": "The focused window receives the typing"},
            ],
            "flows": [["start", "wait"], ["wait", "click"], ["click", "write"], ["write", "hot"], ["hot", "recv"], ["recv", "end"]],
        },
    },
    {
        "id": "ScriptToXServer",
        "pattern": "Interaction",
        "title": "A script sending a click to a window through XTEST",
        "concepts": ["XTestEvents", "SyntheticVersusReal", "ClickSequence", "XtermIgnoresSent"],
        "also_from": ["HowInputIsSent", "BackendSources", "FocusDecides"],
        "read_from": "chapter 23 and the X.Org protocol documents: PyAutoGUI asks the X server to simulate the button events with XTestFakeInput and the window "
                     "receives them",
        "why": "the passage is an exchange between the script, the library and the X server in an order that matters - the request goes out before the window gets the event: an interaction",
        "data": {
            "participants": [
                {"id": "script", "label": "The script"},
                {"id": "lib", "label": "PyAutoGUI"},
                {"id": "xs", "label": "The X server"},
                {"id": "win", "label": "The window"},
            ],
            "messages": [
                ["script", "lib", "Calls click(10, 5)"],
                ["lib", "xs", "Sends XTestFakeInput for the motion"],
                ["lib", "xs", "Sends XTestFakeInput for the button press and release"],
                ["xs", "win", "Delivers the events of the button"],
                ["win", "xs", "Receives the events as if from the real mouse", "reply"],
            ],
        },
    },
    {
        "id": "CopyingTextWithTheClipboard",
        "pattern": "Interaction",
        "title": "A script copying the text of a window through the clipboard",
        "concepts": ["ClipboardRoundTrip", "HotkeyOrder", "FocusDecides"],
        "also_from": ["ClipboardRoute", "WriteString"],
        "read_from": "chapter 23: the program calls pyautogui.hotkey('ctrl', 'a'), then hotkey('ctrl', 'c') and pyperclip.paste() to retrieve the text of a window",
        "why": "the passage is an exchange between the script, the window and the clipboard in an order that matters - the text is copied before it is pasted: an interaction",
        "data": {
            "participants": [
                {"id": "script", "label": "The script"},
                {"id": "win", "label": "The window"},
                {"id": "clip", "label": "The clipboard"},
            ],
            "messages": [
                ["script", "win", "Calls hotkey('ctrl', 'a') to select the text"],
                ["script", "win", "Calls hotkey('ctrl', 'c') to copy the text"],
                ["win", "clip", "Stores the text on the clipboard"],
                ["script", "clip", "Calls pyperclip.paste()"],
                ["clip", "script", "Returns the text of the window", "reply"],
            ],
        },
    },
    {
        "id": "TheLifeOfADrag",
        "pattern": "LifeCycle",
        "title": "A drag from the first press of the button to its release",
        "concepts": ["DragEvents", "DragVersusMove", "ClickSequence", "SpiralDrawing"],
        "also_from": ["DraggingAndScrolling", "MoveRelative", "DurationSteps"],
        "read_from": "chapter 23, Dragging the Mouse: dragTo() and drag() move the cursor with the button held down, in the steps that the duration gives, "
                     "and the button is released at the new location",
        "why": "the passage follows the pointer through the states it is in during a drag and names the call that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "idle", "label": "The cursor is at its place"},
                {"id": "down", "label": "The button is held down"},
                {"id": "moving", "label": "The cursor moves in steps"},
                {"id": "up", "label": "The button is released"},
            ],
            "initial": "idle",
            "final": ["up"],
            "transitions": [
                ["idle", "down", "drag() pushes the button down"],
                ["down", "moving", "The cursor moves for the duration"],
                ["moving", "up", "The button is released at the new location"],
            ],
        },
    },
    {
        "id": "WhatAScriptCanDoWithPyAutoGUI",
        "pattern": "SetOfUses",
        "title": "What a script can do with PyAutoGUI",
        "concepts": ["MovingTheMouse", "Clicking", "DraggingAndScrolling", "Screenshots", "ImageRecognition", "TypingText", "MessageBoxes"],
        "also_from": ["ScrollEvents", "PixelColor", "WriteString", "HotkeyOrder", "MessageBoxResults", "PositionTuple"],
        "read_from": "chapter 23: move the mouse, click, drag and scroll, take a screenshot, find an image on the screen, type text and press hotkeys, and display message boxes",
        "why": "the chapter lists independent things a script can ask the library to do - move, click, drag, scroll, look, type, ask - a set of uses, not a sequence",
        "data": {
            "system": "PYAUTOGUI",
            "actors": [{"id": "script", "label": "A script"}],
            "usecases": [
                {"id": "move", "label": "Move the mouse with moveTo()"},
                {"id": "click", "label": "Click a button with click()"},
                {"id": "drag", "label": "Drag the mouse with drag()"},
                {"id": "scroll", "label": "Scroll with scroll()"},
                {"id": "shot", "label": "Take a screenshot"},
                {"id": "find", "label": "Find an image with locateOnScreen()"},
                {"id": "type", "label": "Type text with write()"},
                {"id": "box", "label": "Show a message box with confirm()"},
            ],
            "links": [["script", "move"], ["script", "click"], ["script", "drag"], ["script", "scroll"], ["script", "shot"], ["script", "find"], ["script", "type"], ["script", "box"]],
        },
    },
    {
        "id": "ControllingTheKeyboardAndMouseAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Controlling the keyboard and mouse at a glance: six branches",
        "concepts": ["InstallingAndSendingInput", "StayingOnTrack", "MouseControl", "ScreenAndImages", "WindowsAndKeyboard", "ScriptsAndPractice"],
        "also_from": ["TheLibraries", "HowInputIsSent", "PausesAndFailSafes", "ScreenCoordinates", "Clicking", "Screenshots", "ImageRecognition", "TypingText", "KeyNames",
                      "HotkeysAndFocus", "MessageBoxes", "PracticeProblems", "XTestEvents", "WaylandSession", "FailsafeFires", "PauseDefault", "ScreenSize", "OriginAndCorners",
                      "DragEvents", "ScrollUnits", "ImageNotFound", "OldScreezeReturnsNone", "WriteString", "KeyTable", "BadKeyName", "FocusDecides", "MessageBoxResults",
                      "LookingBusy", "Interpreters", "TkVersions", "MouseInfoTk9", "LibraryVersion", "XtermIgnoresSent", "WindowFunctionsLinux", "SleepAndCountdown"],
        "read_from": "chapter 23, the opening of each of its main parts: installing and sending input, staying on track, controlling the mouse, the screen and images, "
                     "windows and the keyboard, and scripts and practice",
        "why": "the chapter classifies one topic, controlling a computer with a script, by what each part is about and lists examples under each - a topic and "
               "its parts, laid out to remember, with the one idea that holds for every part stated once at the root",
        "data": {
            "root": "A script controls the mouse and keyboard through synthetic input",
            "branches": [
                {"label": "Installing and sending input",
                 "children": ["PyAutoGUI sends events through XTEST on Linux",
                              "A Wayland session does not accept them",
                              "Window functions exist only on Windows"]},
                {"label": "Staying on track",
                 "children": ["The pause after each call is 0.1 seconds",
                              "A corner of the screen raises the fail-safe",
                              "The exception stops the program"]},
                {"label": "Mouse control",
                 "children": ["The origin (0, 0) is the top left corner",
                              "click() presses and releases the button",
                              "drag() holds the button down"]},
                {"label": "Screen and images",
                 "children": ["screenshot() returns an image",
                              "locateOnScreen() returns a box",
                              "A missing image raises ImageNotFoundException"]},
                {"label": "Windows and keyboard",
                 "children": ["write() types a string",
                              "An unknown key name is ignored",
                              "The focused window receives the typing"]},
                {"label": "Scripts and practice",
                 "children": ["confirm() returns the button clicked",
                              "Looking Busy moves the cursor by one pixel",
                              "Tk 9 breaks MouseInfo"]},
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
    CHX = "http://example.org/sen0414/ch23#"
    d = os.path.join(root, "03-materials", "ch23", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch23_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch23_domain_abox_v1_0_2.ttl"))
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
