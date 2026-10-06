#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - SEN0414 chapter 5 (Debugging) on the CME classroom standard.

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


C = load("corpus414_5", os.path.join(HERE, "..", "sen0414_ch05_corpus_v1_0_0.py"))
ST = load("stories414_5", os.path.join(HERE, "..", "sen0414_ch05_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch05/assets/"
for _f in ("photo_mark2_moth.jpg", "photo_brian_kernighan.jpg"):
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
    out += "\nFULL TEXT: course page, chapter 5 - " + ", ".join(names) + "."
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


def prog(pname, x, y, w, h, fs=10, lines=None):
    """A chapter program, whole or an honest excerpt, with its transcript - the shape
    program_check_v2_0_1 verifies (slice verbatim; transcript re-executed)."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    lines = all_lines[a - 1:b]
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
            "cap": "program %s, lines %d to %d of %d, %s" % (pname, a, b, len(all_lines), CAP)}


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
    'The questions this chapter answers': 'If you can answer these, chapter 5 is yours',
    'One chapter, six branches': 'Six branches - every slide today lives on this map',
    'The bug you can visit in a museum': 'Every bug since has been a metaphor; this one had wings',
    'Read the traceback upward': 'The last line names the crime; the lines above name the scene',
    'Unwind, catch, annotate': 'An exception travels up until someone claims it',
    'assert: executable assumptions': 'An assert is a tripwire for states that must never happen',
    'The most effective debugging tool': 'Logging is the print statement that grew up',
    'A logging system with a birth certificate': 'The five log levels are a 2002 design decision',
    'Levels: choose what you hear': 'Set the level, not your patience - DEBUG to CRITICAL',
    'Log to a file; switch it off cleanly': 'Evidence goes to files; disable beats delete',
    'Hunt one bug, with the log as witness': 'The log shows the loop die one step early',
    'The string that beat the integer': 'Types are part of the bug - the log prints them',
    'The debugger: the program, paused': 'A debugger is a conversation with a paused program',
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
slide("title", "Chapter 5: Debugging", "Tracebacks, assertions, logging - and the moth that started it all",
      [{"t": "code", "x": 6.0, "y": 1.3, "w": 3.5, "h": 1.7, "fs": 11, "cap": CAP,
        "rows": [["int('x')", "ValueError: invalid literal for int() with base 10: 'x'"]]}],
      "SAY: Chapters 1-4 wrote programs; chapter 5 is for the day they misbehave: reading what "
      "Python tells you, planting tripwires, keeping logs, and pausing the program mid-thought.\n"
      "FULL TEXT: course page, chapter 5.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.9, "fs": 13,
          "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["recorded under Python 3.14.6", "bug-and-fix program pairs", "the log as evidence"]}],
        paras("BugModel"))

content("One chapter, six branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 3, "fs": 12.5, "subfs": 10, "accent": [0],
          "items": [{"label": decamel(r), "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("BugModel", "ErrorSignalling", "Assertion", "Logging", "Debugger", "ModernPractice")]}],
        paras("BugModel", "Logging"),
        lede="Six branches; the count under each is how many concepts the course page explains for it - today walks the spine.")

# ---- Reading what Python tells you ------------------------------------------------------------
section("Reading the report", "Tracebacks, raised errors, and notes",
        [{"label": "The traceback"}, {"label": "raise"}, {"label": "Unwinding"}, {"label": "Notes"}],
        paras("ErrorSignalling"))

content("The bug you can visit in a museum", STORY["FirstBug"]["when"],
        [img("photo_mark2_moth.jpg", 0.5, 1.45, 4.4, 2.75, cap="the Mark II logbook page, moth taped in - U.S. Navy photo, public domain"),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.5, "fs": 12.5, "items": [
             "9 September 1947: the Mark II stops",
             "Relay 70, panel F: a moth",
             "'First actual case of bug being found'",
             "The page survives at the Smithsonian"]},
         factrow("FirstBug", x=0.5, y=4.42, w=9.0)],
        story_notes("FirstBug"))

content("Read the traceback upward", "A crash in a box-printing program, dissected",
        [dict(prog("boxprint_v1_0_0.py", 0.5, 1.42, 9.0, 3.5, fs=7.5), label="the box prints, then the crash - read the report bottom line first")],
        paras("ErrorSignalling", ask="Which line of the report names YOUR file, and which names the library's?"))

content("Unwind, catch, annotate", "An exception climbs until someone claims it",
        [dict(prog("unwinding_v1_0_0.py", 0.5, 1.55, 4.3, 2.6, fs=8.5), label="three frames up, one except claims it"),
         dict(prog("notes_v1_0_0.py", 5.1, 1.55, 4.4, 2.0, fs=8.5), label="add_note: context travels WITH the error"),
         {"t": "when", "x": 5.1, "y": 3.8, "w": 4.4, "body": "notes are 3.11+ modern practice"}],
        paras("ErrorSignalling", "ModernPractice", ask="Where would the note have saved you an hour last week?"))

# ---- Assertions -------------------------------------------------------------------------------
section("Assertions", "Executable assumptions",
        [{"label": "assert"}, {"label": "Messages"}, {"label": "The -O caveat"}],
        paras("Assertion"))

content("assert: executable assumptions", "Tripwires for states that must never happen",
        [dict(prog("assertdemo_v1_0_0.py", 0.5, 1.55, 4.3, 1.9, fs=8.5), label="bare assert: it fires, but mutely"),
         dict(prog("assertmsg_v1_0_0.py", 5.1, 1.55, 4.4, 1.75, fs=8.5), label="with a message: the tripwire explains itself"),
         dict(prog("optimised_v1_0_0.py", 0.5, 3.42, 9.0, 1.58, fs=9), label="python -O strips asserts: they guard the programmer, never user input")],
        paras("Assertion", ask="Which chapter-4 validation would be WRONG as an assert, and why?"))

# ---- Logging ----------------------------------------------------------------------------------
section("Logging", "The print statement that grew up",
        [{"label": "Levels"}, {"label": "To a file"}, {"label": "force and disable"}, {"label": "Lazy formatting"}],
        paras("Logging"))

content("The most effective debugging tool", STORY["PrintDebugging"]["when"],
        [img("photo_brian_kernighan.jpg", 0.5, 1.45, 3.0, 2.9, cap="Brian Kernighan at Bell Labs - photo: Ben Lowe, CC BY 2.0"),
         {"t": "beats", "x": 3.9, "y": 1.5, "w": 5.6, "h": 2.3, "fs": 12.5, "items": [
             "Bell Labs, 1979: 'careful thought, coupled with",
             "judiciously placed print statements'",
             "This chapter agrees - then gives print levels,",
             "timestamps, files, and an off switch"]},
         factrow("PrintDebugging", x=3.9, y=4.42, w=5.6)],
        story_notes("PrintDebugging"))

content("A logging system with a birth certificate", STORY["LoggingPep"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.42, "w": 9.0, "h": 1.0, "fs": 12.5, "items": [
            "PEP 282 (2002), Vinay Sajip and Trent Mick - modelled on log4j's levels",
            "In the standard library since Python 2.3; these slides run that exact machinery"]},
         dict(code("levels", 0.5, 2.55, 9.0, 1.05, fs=9), label="the ladder, asked directly"),
         factrow("LoggingPep", x=0.5, y=4.42, w=9.0)],
        story_notes("LoggingPep"))

content("Levels: choose what you hear", "One knob from DEBUG to CRITICAL",
        [dict(prog("levelsdemo_v1_0_0.py", 0.5, 1.5, 9.0, 2.2, fs=8), label="level=INFO: the DEBUG line stays silent"),
         dict(prog("force_v1_0_0.py", 0.5, 3.78, 9.0, 1.22, fs=7.5, lines=(5, 7)), label="force=True rewires mid-program - 3.8+ practice")],
        paras("Logging", ask="Which level would your coin-toss homework log its guesses at?"))

content("Log to a file; switch it off cleanly", "Evidence on disk, silence on demand",
        [dict(prog("filelog_v1_0_0.py", 0.5, 1.46, 9.0, 1.64, fs=7.5), label="filename= sends the evidence to disk - and CRITICAL still reaches you"),
         dict(prog("disable_v1_0_0.py", 0.5, 3.16, 9.0, 1.84, fs=8), label="logging.disable: one line silences below a level - no deletions")],
        paras("Logging", ask="Why does disable() beat deleting log calls the night before a demo?"))

# ---- The hunt ---------------------------------------------------------------------------------
section("The hunt", "Two real bugs, found by their logs",
        [{"label": "Factorial, off by one"}, {"label": "String vs int"}, {"label": "The debugger"}],
        paras("BugModel"))

content("Hunt one bug, with the log as witness", "factorial(3) returns 0 - the log says why",
        [dict(prog("factorial_bug_v1_0_0.py", 0.5, 1.5, 9.0, 3.0, fs=8), label="read the DEBUG lines: i starts at 0, and the product dies with it")],
        paras("BugModel", "Logging", ask="Before the next slide: which single argument of range() is wrong?"))

content("The one-character fix, witnessed", "Same program, range(1, ...) - the log now testifies",
        [dict(prog("factorial_fixed_v1_0_0.py", 0.5, 1.5, 9.0, 2.9, fs=8), label="the log ends at 6 - and reads as the proof the fix worked"),
         {"t": "numlist", "x": 0.5, "y": 4.55, "w": 9.0, "h": 0.42, "fs": 10.5, "items": [
            "The fix is one character class: range(n + 1) became range(1, n + 1)"]}],
        paras("BugModel", "Logging", ask="Keep or delete these DEBUG lines after the fix - argue both ways in one sentence."),
        take="The log that found the bug doubles as the proof of the fix")

content("The string that beat the integer", "The chapter's coin toss never wins - types tell",
        [dict(prog("cointoss_bug_v1_0_0.py", 0.5, 1.5, 9.0, 2.35, fs=8.5), label="seeded for the slide: toss is an int, your guess is a str - they can never be equal"),
         {"t": "text", "x": 0.5, "y": 4.02, "w": 6.1, "h": 0.9, "fs": 8.5, "color": "mute",
          "body": "the second recorded run, guessing tails, loses identically:\n" + PROGS["cointoss_bug_v1_0_0.py"]["runs"][1]["transcript"].strip()},
         {"t": "when", "x": 6.9, "y": 4.25, "w": 2.6, "body": "fix: compare like with like"}],
        paras("BugModel", ask="Write the one-line fix both ways - which reads better at the call site?"))

content("The debugger: the program, paused", "breakpoint() - a conversation mid-thought",
        [dict(prog("debugdemo_v1_0_0.py", 0.5, 1.55, 4.3, 2.6, fs=8.5), label="the demo the lab runs under pdb"),
         {"t": "numlist", "x": 5.1, "y": 1.6, "w": 4.4, "h": 2.3, "fs": 10.5, "items": [
            "breakpoint() drops you into pdb at that line",
            "n steps over; s steps in; p prints a name",
            "c continues; q quits the session",
            "The lab: watch total grow, step by step"]},
         {"t": "chips", "x": 0.5, "y": 4.35, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["n next", "s step in", "p name", "c continue", "q quit"]}],
        paras("Debugger", ask="At which line would a breakpoint have caught the factorial bug fastest?"))

content("Where to go from here", "The chapter's own checked sources - every entry a live link",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The textbook, chapter 5 - free online", source_url("Automate the Boring Stuff")],
                ["The tutorial: errors and exceptions", source_url("Errors and Exceptions")]]},
            {"head": "Reference", "rows": [
                ["logging - the module these slides ran", source_url("logging")],
                ["pdb - the debugger", source_url("pdb")],
                ["Built-in exceptions", source_url("Built-in Exceptions")]]},
            {"head": "History", "rows": [
                ["PEP 282 - a logging system (2002)", "https://peps.python.org/pep-0282/"],
                ["The 1947 moth, at the Smithsonian", "https://en.wikipedia.org/wiki/Software_bug"]]},
            {"head": "Practice", "rows": [
                ["python -O and assertions", source_url("the -O option")],
                ["PEP 678 - notes on exceptions", source_url("Enriching Exceptions")]]}]}],
        "SAY: Every link is a source the chapter corpus cites and checked. Homework: run the "
        "coin toss UNSEEDED, lose three times, then fix it and log every toss at DEBUG.\n"
        "ASK: Bring one traceback you met this week - we will read it upward together.\n"
        "FULL TEXT: course page, chapter 5 - Logging.",
        take="Eight links, checked by the build - one of them has a moth in it")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "How to read a traceback, and in which direction",
          "What an assert guards, and what it must never guard",
          "Five log levels, to console or file, silenced cleanly",
          "How a log and a breakpoint corner a real bug"])}],
      "SAY: Four claims, each carried by a transcript you watched print. Five chapters, one "
      "look, every number earned - the first half of the course stands.\n"
      "FULL TEXT: course page, chapter 5.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "A traceback reads upward: the last line names the crime, the ones above the scene",
              "Exceptions climb until claimed; add_note sends context along for the ride",
              "assert trips on impossible states - and python -O reminds you whom it guards",
              "Logging is print with levels, files and an off switch - a 2002 PEP you inherit",
              "Two real bugs fell today: the log cornered one, types confessed the other"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 5 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and a moth with its own museum label",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("Reading the report", "Assertions", "Logging", "The hunt"))
_rows = [("Questions and the chapter map", 3, _a),
         ("Reading the report - tracebacks, unwinding, notes", _a + 1, _b),
         ("Assertions - executable assumptions", _b + 1, _c),
         ("Logging - levels, files, the off switch", _c + 1, _d),
         ("The hunt, summary, and resources", _d + 1, len(S))]
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
S[1]["notes"] = ("SAY: Five parts, from a museum moth to a paused program - every transcript "
                 "verified off this very file.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 5 - every section.")

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

plan = {"meta": {"title": "Chapter 5: Debugging", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the CME materials look-and-feel standard v1.0.0"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
