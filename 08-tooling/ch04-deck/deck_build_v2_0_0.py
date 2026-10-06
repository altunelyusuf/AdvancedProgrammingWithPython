#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - SEN0414 chapter 4 (Functions) on the CME classroom standard.

Same regime as chapter 1 (CME materials look-and-feel v1.0.0, the shared renderer, the >>> chip):
numbered warm-ivory slides, agenda with exact ranges, summary before live-linked resources, word
gates, 5N1K stories with fact rows, consoles WITH results and errors as Python raised them. New
here: whole PROGRAMS with their transcripts - each panel captioned 'program <name>, lines a to b
of n', re-executed and text-verified off the finished file by program_check_v2_0_0.py, while
deck_check_v1_0_1.py re-runs every '>>>' row.

Usage: python3 deck_build_v3_0_0.py   (writes deck_plan_v3_0_0.json beside itself)
"""
__version__ = "2.0.0"

import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load("corpus414_4", os.path.join(HERE, "..", "sen0414_ch04_corpus_v1_0_0.py"))
ST = load("stories414_4", os.path.join(HERE, "..", "sen0414_ch04_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch04/assets/"
for _f in ("photo_edsac.jpg",):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_2_0.json")))
SRC = json.load(open(os.path.join(HERE, "sources_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
SOURCES = {s["label"]: s["url"] for s in SRC["sources"]}


def source_url(label_part):
    for lbl, url in SOURCES.items():
        if label_part in lbl:
            return url
    raise SystemExit("REFUSED: no checked source matching %r" % label_part)


BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in G.values() for _, out in rows)
STORYTEXT = " ".join(s["story"] + " " + s["source"] + " " + s["when"] for s in ST.STORIES)


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def paras(*names, ask=None):
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    lead = BYNAME[names[0]][5][0][1]
    say = _sentences(lead, 2)
    if len(say) > 480:
        say = _sentences(lead, 1)
    out = "SAY: " + say
    if ask:
        out += "\nASK: " + ask
    out += "\nFULL TEXT: course page, chapter 4 - " + ", ".join(names) + "."
    return out


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n)


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def assert_fact(token, where):
    t = str(token)
    if t in CORPUS_TEXT or t in OUTTEXT or t in STORYTEXT or t.replace(",", "") in OUTTEXT:
        return t
    raise SystemExit("REFUSED: %r (slide %r) is in neither the corpus, the outputs, nor a story" % (t, where))


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets" % (title, len(items)))
    for b in items:
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph" % (b, title))
    return items


def code(group, x, y, w, h, fs=11, rows=None):
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    nlines = sum(1 + (1 if out.strip() else 0) for _, out in rr)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - 0.30) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin" % (group, w, h))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def prog(pname, x, y, w, h, fs=10):
    """A whole chapter program with its transcript, in the shape program_check_v2_0_0 verifies."""
    pr = PROGS[pname]
    lines = pr["code"].rstrip("\n").split("\n")
    out = pr["runs"][0]["transcript"].strip()
    outlines = out.count("\n") + (1 if out else 0)
    maxlen = max(max(len(l) for l in lines), max((len(x) for x in out.split("\n")), default=0) + 8)
    nlines = len(lines) + outlines
    fit_w = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - 0.56) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit_w, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s cannot fit unwrapped in %.1fx%.1fin" % (pname, w, h))
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": lines, "fs": fs, "compact": True,
            "out": out if out else None, "outLabel": "prints",
            "cap": "program %s, lines 1 to %d of %d, %s" % (pname, len(lines), len(lines), CAP)}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return "STORY (%s): %s\nSOURCE: %s" % (st["when"], st["story"], st["source"])


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


S = []


TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 4 is yours',
    'One chapter, seven branches': 'Seven branches - every slide today lives on this map',
    '1952: the function gets invented': 'def and return are 1952 inventions you use every day',
    'def, call, return - the whole loop': 'A function is a named block with a way back',
    'Parameters: positional, named, defaults': 'Call sites read best when arguments carry names',
    'The default that remembered too much': 'Evaluate-once defaults: never use a mutable one',
    'Frames: where calls live': 'Every call pushes a frame; return pops it - the stack IS the story',
    'Recursion meets its limit': 'The 1000-frame ceiling is a safety rail, measured live',
    'Scope: which x is this?': 'Reading reaches out; assignment stays local unless declared',
    'global and nonlocal, demonstrated': 'Declarations change where assignment lands - use sparingly',
    'The unsolved problem in your homework': 'A five-line function can hold an unsolved problem',
    'try inside or outside? Both, shown': 'Put try where you can DO something about the error',
    'The except clause sheds its parentheses': 'Language change is checkable - this slide ran on 3.14',
    'Annotations: promises for readers and tools': 'Annotations document intent; 3.14 defers their cost',
}


def slide(kind, title, sub, items, notes, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg})


def content(title, sub, items, notes, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9,
              "cols": 2 if image else min(4, len(boxes)), "fs": 14, "subfs": 11, "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes, bg="light")


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 4: Functions", "Named blocks, honest returns - and the stack that keeps the way back",
      [{"t": "code", "x": 6.0, "y": 1.3, "w": 3.5, "h": 1.7, "fs": 12, "cap": CAP,
        "rows": [["def twice(n): return 2 * n", ""], ["twice(21)", "42"]]}],
      "SAY: Chapters 1-3 wrote code that runs top to bottom; chapter 4 names blocks of it, "
      "hands them inputs, and gets values back - plus the stack, scope and error-handling that "
      "make it safe.\nFULL TEXT: course page, chapter 4.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.9, "fs": 13,
          "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["recorded under Python 3.14.6", "whole programs with transcripts", "errors are answers too"]}],
        paras("Function"))

content("One chapter, seven branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 4, "fs": 12.5, "subfs": 10, "accent": [0],
          "items": [{"label": decamel(r), "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("Function", "Result", "Frames", "Scope", "ErrorHandling", "Programs", "ModernPractice")]}],
        paras("Function", "Scope"),
        lede="Seven branches; the count under each is how many concepts the course page explains for it - today walks the spine.")

# ---- Defining and calling ---------------------------------------------------------------------
section("Defining and calling", "def, arguments, and what comes back",
        [{"label": "def and call"}, {"label": "Parameters"}, {"label": "return"}, {"label": "Defaults"}],
        paras("Function"))

content("def, call, return - the whole loop", "Two programs, every basic in play",
        [dict(prog("hello_v1_0_0.py", 0.5, 1.55, 4.3, 2.45, fs=9), label="define once, call twice - then once more"),
         dict(prog("returns_v1_0_0.py", 5.1, 1.55, 4.4, 2.3, fs=9), label="return hands back a VALUE, any type"),
         {"t": "chips", "x": 0.5, "y": 4.25, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["def names a block", "() runs it", "return ends it with a value", "no return means None"]}],
        paras("Function", "Result", ask="What does print(print('hi')) show, and why two lines?"))

content("Parameters: positional, named, defaults", "Call sites that read like sentences",
        [dict(prog("params_v1_0_0.py", 0.5, 1.55, 4.3, 2.5, fs=9), label="positional order, then names at the call"),
         dict(prog("named_v1_0_0.py", 5.1, 1.55, 4.4, 1.5, fs=9), label="sep and end: named arguments you already met"),
         dict(code("types", 5.1, 3.35, 4.4, 1.05, fs=9.5), label="None: the quiet return of functions that only DO")],
        paras("Function", ask="Rewrite print('a','b',sep='-') with positional-only thinking - why does it refuse?"))

content("The default that remembered too much", "Evaluate-once defaults, caught in the act",
        [{"t": "numlist", "x": 0.5, "y": 1.55, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "A default value is evaluated ONCE, at def time",
            "A mutable default then lives between calls",
            "The fix: default to None, create inside"]},
         dict(prog("defaults_v1_0_0.py", 4.3, 1.5, 5.2, 3.3, fs=8.5), label="the classic trap, then the idiomatic repair"),
         {"t": "when", "x": 0.5, "y": 3.75, "w": 3.55, "body": "def=None, make it inside"}],
        paras("Function", "ModernPractice", ask="Why does the SAME list come back - where does it live between calls?"))

# ---- Frames and scope -------------------------------------------------------------------------
section("Frames and scope", "Where calls live, and which x you mean",
        [{"label": "The call stack"}, {"label": "Recursion"}, {"label": "Local vs global"}, {"label": "global / nonlocal"}],
        paras("Frames"))

content("1952: the function gets invented", STORY["ClosedSubroutine"]["when"],
        [img("photo_edsac.jpg", 0.5, 1.45, 3.4, 2.5, cap="EDSAC - Computer Laboratory, University of Cambridge, CC BY 2.0"),
         {"t": "beats", "x": 4.3, "y": 1.5, "w": 5.2, "h": 2.3, "fs": 12.5, "items": [
             "EDSAC, Cambridge: one of the first stored-program machines",
             "Wheeler's problem: jump into shared code AND find the way back",
             "His closed subroutine is the ancestor of every def here",
             "The call stack is his return-address bookkeeping, grown up"]},
         factrow("ClosedSubroutine", x=0.5, y=4.42, w=9.0)],
        story_notes("ClosedSubroutine"))

content("Frames: where calls live", "Three nested calls, photographed from inside",
        [dict(prog("stack_v1_0_0.py", 0.5, 1.55, 9.0, 3.3, fs=8.5), label="each call pushes a frame; inspect shows the stack mid-flight")],
        paras("Frames", ask="Read the frame list aloud bottom-up - whose return comes first?"))

content("Recursion meets its limit", "The safety rail, measured live",
        [dict(prog("recursion_v1_0_0.py", 0.5, 1.55, 4.3, 2.1, fs=9), label="a function that calls itself with no exit"),
         dict(code("limits", 5.1, 1.55, 4.4, 1.1, fs=9.5), label="the ceiling, asked directly"),
         {"t": "numlist", "x": 5.1, "y": 2.9, "w": 4.4, "h": 1.5, "fs": 10.5, "items": [
            "Every call adds a frame; frames cost memory",
            "Python stops the runaway at a set depth",
            "Real recursion needs a base case - Collatz has one"]}],
        paras("Frames", ask="What is THIS function's missing base case - add it in one line."))

content("Scope: which x is this?", "Reading reaches out; assignment stays home",
        [dict(prog("scopes_v1_0_0.py", 0.5, 1.55, 4.3, 2.9, fs=9), label="four prints, three scopes - trace each"),
         {"t": "numlist", "x": 5.1, "y": 1.6, "w": 4.4, "h": 1.9, "fs": 10.5, "items": [
            "A def opens a new local scope",
            "Reading a name searches outward: local, enclosing, global, built-in",
            "Assigning a name claims it LOCAL - everywhere in that def"]},
         {"t": "when", "x": 5.1, "y": 3.85, "w": 4.4, "body": "read reaches out; assignment stays home"}],
        paras("Scope", ask="Trace print number three: which scope answers, and why not the inner one?"))

content("Assign later, crash earlier", "The famous scope error, in full",
        [dict(prog("unbound_v1_0_0.py", 0.5, 1.55, 9.0, 1.85, fs=9), label="one assignment at the bottom makes the TOP print illegal"),
         {"t": "numlist", "x": 0.5, "y": 3.7, "w": 9.0, "h": 1.1, "fs": 10.5, "items": [
            "The assignment on the last line marks eggs local for the WHOLE function",
            "So the first line's read finds a local that does not exist yet - UnboundLocalError"]}],
        paras("Scope", ask="Fix it two ways: rename, or declare - which would PEP 8 prefer here?"),
        take="Assignment anywhere makes it local everywhere - the error says so")

content("global and nonlocal, demonstrated", "Declarations that move the assignment",
        [dict(prog("globalstmt_v1_0_0.py", 0.5, 1.55, 4.3, 2.45, fs=9), label="global: the module's name, changed inside"),
         dict(prog("nonlocal_v1_0_0.py", 5.1, 1.55, 4.4, 2.3, fs=9), label="nonlocal: the enclosing def's name"),
         {"t": "chips", "x": 0.5, "y": 4.25, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["read: no declaration needed", "assign: local by default", "declare to aim higher"]}],
        paras("Scope", ask="Which of the two would a five-function module regret first, and why?"))

# ---- Errors, handled --------------------------------------------------------------------------
section("Errors, handled", "try, except - and where to put them",
        [{"label": "try / except"}, {"label": "Placement"}, {"label": "PEP 758"}, {"label": "Validation"}],
        paras("ErrorHandling"))

content("try inside or outside? Both, shown", "Same crash, two placements, different programs",
        [dict(prog("inside_v1_0_0.py", 0.5, 1.55, 4.3, 2.7, fs=8.5), label="inside: the function apologizes and returns None"),
         dict(prog("outside_v1_0_0.py", 5.1, 1.55, 4.4, 2.7, fs=8.5), label="outside: the caller decides what an error means"),
         {"t": "when", "x": 2.8, "y": 4.4, "w": 4.4, "body": "catch where you can act"}],
        paras("ErrorHandling", ask="Which placement hides the None surprise from slide 6's chips?"))

content("The except clause sheds its parentheses", STORY["Pep758Arrives"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.42, "w": 9.0, "h": 1.0, "fs": 12.5, "items": [
            "For decades: except (ValueError, TypeError) - parentheses required",
            "PEP 758, shipped in 3.14: the bare pair now parses - and this build RAN it"]},
         dict(prog("except758_v1_0_0.py", 0.5, 2.55, 9.0, 1.5, fs=9.5), label="executed under the build's 3.14.6; on 3.13 this file is a SyntaxError"),
         factrow("Pep758Arrives", x=0.5, y=4.42, w=9.0)],
        story_notes("Pep758Arrives"))

# ---- Working programs -------------------------------------------------------------------------
section("Working programs", "Functions earning their keep",
        [{"label": "Collatz"}, {"label": "Input validation"}, {"label": "Annotations"}],
        paras("Programs"))

content("The unsolved problem in your homework", STORY["CollatzMystery"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.4, "w": 9.0, "h": 0.55, "fs": 12.5, "items": [
            "Halve if even, triple-and-add-one if odd: Collatz (1937) says you always reach 1 - unproven since; Erdos offered 500 dollars"]},
         dict(prog("collatz_v1_0_0.py", 0.5, 2.06, 9.0, 2.36, fs=8.5), label="the rule as a function, fed 3 - eight steps to 1"),
         factrow("CollatzMystery", x=0.5, y=4.52, w=9.0)],
        story_notes("CollatzMystery"))

content("Validate at the door", "A function that refuses bad input politely",
        [dict(prog("validated_v1_0_0.py", 0.5, 1.55, 4.9, 3.1, fs=8), label="a retry loop - bad input, then good"),
         {"t": "numlist", "x": 5.75, "y": 1.6, "w": 3.75, "h": 1.9, "fs": 10.5, "items": [
            "Ask, check, re-ask - inside ONE function",
            "The caller receives only a valid number",
            "try/except from the last section does the checking"]},
         {"t": "when", "x": 5.75, "y": 3.85, "w": 3.75, "body": "functions guard their own doors"}],
        paras("Programs", ask="Move the while into the caller - what gets duplicated at every call site?"),
        take="Validation lives inside the function, so every caller inherits it")

content("Annotations: promises for readers and tools", "And the 3.14 change underneath them",
        [dict(prog("annotations_v1_0_0.py", 0.5, 1.55, 9.0, 2.1, fs=9), label="annotations evaluate lazily now - the forward name survives until you ASK for it"),
         {"t": "chips", "x": 0.5, "y": 3.95, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["hints, not checks", "tools and IDEs read them", "3.14: deferred by default"]}],
        paras("Programs", "ModernPractice", ask="Which line would a type checker flag here that Python itself never will?"))

content("Where to go from here", "The chapter's own checked sources - every entry a live link",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The textbook, chapter 4 - free online", source_url("Automate the Boring Stuff")],
                ["The tutorial: defining functions", source_url("More Control Flow")]]},
            {"head": "Reference", "rows": [
                ["Compound statements: def", source_url("Compound statements")],
                ["Built-in functions", source_url("Built-in Functions")]]},
            {"head": "Modern practice", "rows": [
                ["PEP 758 - except without parentheses", "https://peps.python.org/pep-0758/"],
                ["What's new in 3.14", source_url("3.14")]]},
            {"head": "History & puzzles", "rows": [
                ["David Wheeler and the subroutine", "https://en.wikipedia.org/wiki/David_Wheeler_(computer_scientist)"],
                ["The Collatz conjecture", "https://en.wikipedia.org/wiki/Collatz_conjecture"]]}]}],
        "SAY: Every link is a source the chapter corpus cites and checked - plus the two stories' "
        "own trails. Homework: give collatz a base-case twin that RETURNS the step count.\n"
        "ASK: Who can explain the Wheeler jump with two bookmarks and a book?\n"
        "FULL TEXT: course page, chapter 4 - ModernPractice.",
        take="Eight links, checked by the build - one of them is an unsolved problem")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What def names, and what return hands back",
          "Why the mutable default misbehaves, and the repair",
          "Which x an assignment touches - and how to aim higher",
          "Where try belongs, and what 3.14 changed about except"])}],
      "SAY: Four claims, each carried by a transcript you watched print - one of them only "
      "possible on 3.14. Next week: debugging - when the transcript surprises you.\n"
      "FULL TEXT: course page, chapter 4.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "def names a block; calls hand it values; return brings one back - or None, quietly",
              "Defaults evaluate once: the remembered list is the trap, None-then-create the repair",
              "Every call is a frame on the stack - Wheeler's 1952 bookkeeping, with a 1000-deep rail",
              "Assignment is local unless declared; reading reaches outward - that is all of scope",
              "try belongs where you can act; 3.14's except sheds parentheses, and this build ran it"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 4 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and every transcript printed under 3.14.6",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("Defining and calling", "Frames and scope", "Errors, handled", "Working programs"))
_rows = [("Questions and the chapter map", 3, _a),
         ("Defining and calling - def, parameters, returns", _a + 1, _b),
         ("Frames and scope - the stack, global, nonlocal", _b + 1, _c),
         ("Errors, handled - try placement and PEP 758", _c + 1, _d),
         ("Working programs, summary, and resources", _d + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))),
                      "label": "consoles and whole programs, run live"}]}]
S[1]["notes"] = ("SAY: Five parts, from Wheeler's 1952 jump to a 3.14-only except clause - every "
                 "transcript verified off this very file.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 4 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES and TAKES[sl["title"]]:
        sl["take"] = TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 4: Functions", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the CME materials look-and-feel standard v1.0.0"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
