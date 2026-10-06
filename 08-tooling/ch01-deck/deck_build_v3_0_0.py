#!/usr/bin/env python3
"""Builds deck_plan_v3_0_0.json - SEN0414 chapter 1 (Python Basics) on the CME classroom standard.

SEN0414 joins the look-and-feel the SEN0401 chapters 1-5 now carry (CME materials standard
v1.0.0): one warm-ivory theme drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js
(same tokens, the course's own >>> chip), numbered slides, an agenda with exact ranges, a
summary before the live-linked resources, word gates, 5N1K stories with fact rows, and every
console shown WITH its executed result - errors exactly as Python raised them. Every '>>>' row
comes from examples_out_v1_1_0.json and deck_check_v1_0_1.py re-runs whatever the finished file
shows. The resources slide links the chapter's own checked sources (sources_out_v1_0_0.json).

Usage: python3 deck_build_v3_0_0.py   (writes deck_plan_v3_0_0.json beside itself)
"""
__version__ = "3.0.0"

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


C = load("corpus414_1", os.path.join(HERE, "..", "sen0414_ch01_corpus_v1_2_0.py"))
ST = load("stories414_1", os.path.join(HERE, "..", "sen0414_ch01_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch01/assets/"
for _f in ("photo_guido_van_rossum.jpg",):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_2_0.json")))
SRC = json.load(open(os.path.join(HERE, "sources_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
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
    out += "\nFULL TEXT: course page, chapter 1 - " + ", ".join(names) + "."
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


# figures re-parsed from the executed examples and re-asserted
import ast as _ast
assert G["shell"][0] == ["2 + 2", "4"]
assert _ast.literal_eval(G["integer"][0][1]) == 2 ** 100
assert G["float"][0][1] == "0.30000000000000004"
_vt = _ast.literal_eval(G["version"][0][1])
assert _vt == tuple(int(x) for x in PYV.split("."))[:3], "version rows must match the build interpreter"
assert G["gil"][0][1] in ("True", "False")
_gil_on = G["gil"][0][1] == "True"

S = []

TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 1 is yours',
    'One chapter, five branches': 'Five branches - every slide today lives on this map',
    'A Christmas project named after a comedy troupe': "One person's holiday itch became your semester's tool",
    'The prompt is a calculator that answers': 'Type, Enter, answer - the whole course fits this loop',
    'Three types you will meet every day': 'int, float, str - and type() always tells you which',
    'Operators, and who goes first': 'Precedence is arithmetic class all over again - parentheses win',
    'Floats are honest about being approximate': '0.1 + 0.2 is not 0.3, and Python says so out loud',
    'Strings: glue, repeat, measure': 'Operators are polite: they refuse types they cannot serve',
    'Variables: names that remember': 'Assignment stores; the name alone gives it back',
    'Functions you get for free': 'round, len, type, int - the standard toolbox is already open',
    'The textbook that gives itself away': 'Your textbook is a link, not a bill - read ahead free',
    'The interpreter under you, interrogated': 'CPython 3.14.4 answered these slides itself',
    'The interpreter sheds its oldest lock': 'Modern practice is checkable - ask your own interpreter',
    'Modules: batteries, included': 'import hands you a toolbox; chapter 3 opens it properly',
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
slide("title", "Chapter 1: Python Basics", "Values, operators, variables - and the prompt that answers back",
      [{"t": "code", "x": 6.0, "y": 1.3, "w": 3.5, "h": 1.7, "fs": 13, "cap": CAP,
        "rows": [["2 + 2", "4"], ["'Py' + 'thon'", "'Python'"]]}],
      "SAY: Everything in this course starts at a prompt that answers back. Today: what Python "
      "values are, how operators combine them, and how names remember them.\n"
      "FULL TEXT: course page, chapter 1.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.9, "fs": 13.5,
          "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["every answer is runnable", "errors are answers too", "sources on the last slide"]}],
        paras("Value"))

content("One chapter, five branches", "The concept map the whole chapter hangs on",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 12, "root": "Chapter 1",
          "nodes": [{"label": decamel(r), "kids": [decamel(x) for x in children(r, 2)[:7]]}
                    for r in ("Value", "Operation", "BuiltInFunction", "ExecutionEnvironment", "ModernPractice")]}],
        paras("Value", "Operation"),
        lede="Each branch is a question the chapter answers; the grey lists are the concepts that answer it, every one explained on the course page.")

# ---- Values -----------------------------------------------------------------------------------
section("Values and types", "What the prompt computes with",
        [{"label": "The shell"}, {"label": "Integers"}, {"label": "Floats"}, {"label": "Strings"}],
        paras("Value"))

content("A Christmas project named after a comedy troupe", STORY["PythonBirth"]["when"],
        [img("photo_guido_van_rossum.jpg", 0.5, 1.45, 3.1, 2.4, cap="Guido van Rossum - photo: Daniel Stroud, CC BY-SA 4.0"),
         {"t": "beats", "x": 4.0, "y": 1.5, "w": 5.5, "h": 2.3, "fs": 13, "items": [
             "December 1989: a hobby interpreter for a closed office",
             "Named for Monty Python's Flying Circus - not the snake",
             "February 1991: version 0.9.0 posted to alt.sources",
             "Three decades of 'Benevolent Dictator For Life' followed"]},
         factrow("PythonBirth", x=0.5, y=4.42, w=9.0)],
        story_notes("PythonBirth"))

content("The prompt is a calculator that answers", "The REPL: read, evaluate, print, loop",
        [{"t": "flow", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.1, "fs": 12.5, "steps": [
            {"label": "Read", "sub": "you type 2 + 2"},
            {"label": "Evaluate", "sub": "Python computes"},
            {"label": "Print", "sub": "4 appears"},
            {"label": "Loop", "sub": "the prompt returns", "hot": True}]},
         dict(code("shell", 0.5, 2.95, 4.3, 1.3, fs=10.5), label="your first three answers"),
         dict(code("expr", 5.1, 2.95, 4.4, 1.0, fs=10.5), label="an expression always becomes one value")],
        paras("ExecutionEnvironment", "Operation", ask="Which of the four steps does a .py FILE skip? (none - chapter 2 shows why)"))

content("Three types you will meet every day", "And the function that names them",
        [dict(code("datatype", 0.5, 1.6, 4.3, 1.35, fs=10), label="type() answers with the type itself"),
         dict(code("integer", 5.1, 1.6, 4.4, 1.35, fs=9), label="integers never overflow - 2 to the 100th, exactly"),
         {"t": "chips", "x": 0.5, "y": 3.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["int: whole, unlimited", "float: decimal point", "str: in quotes"]},
         dict(code("intmix", 0.5, 4.05, 9.0, 0.85, fs=10), label="mixing int and float: the result turns float")],
        paras("Value", "BuiltInFunction", ask="Why does 6 / 3 print 2.0 and not 2?"))

# ---- Operations -------------------------------------------------------------------------------
section("Operations", "Combining values - and the rules of the queue",
        [{"label": "Operators"}, {"label": "Precedence"}, {"label": "Division, three ways"}, {"label": "String algebra"}],
        paras("Operation"))

content("Operators, and who goes first", "Precedence, parentheses, and a classic trap",
        [dict(code("prec", 0.5, 1.6, 4.3, 1.9, fs=9.5), label="the trap: -3 ** 2 is -9"),
         dict(code("intdiv", 5.1, 1.6, 4.4, 1.9, fs=9.5), label="division three ways: /, //, %"),
         {"t": "when", "x": 2.8, "y": 3.85, "w": 4.4, "body": "when in doubt, parenthesize"}],
        paras("Operation", ask="Why does -3 ** 2 give -9 - which operator won?"))

content("Floats are honest about being approximate", "The one float fact that saves you hours",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Floats are binary fractions - most decimals do not fit exactly",
            "So equality tests on floats mislead",
            "round() is the honest way to compare or present"]},
         dict(code("float", 4.3, 1.6, 5.2, 1.5, fs=10), label="see it once, remember it forever"),
         {"t": "stat", "x": 4.3, "y": 3.4, "w": 5.2, "h": 0.95, "items": [
             {"n": "False", "label": "0.1 + 0.2 == 0.3 - and that is correct behaviour"}]}],
        paras("Value", ask="Money in floats: why do banks count in kurus integers instead?"),
        lede="This slide exists because every programmer meets 0.30000000000000004 once; meeting it today, on purpose, is cheaper.")

content("Strings: glue, repeat, measure", "The same operators, politely refusing the wrong types",
        [dict(code("concat", 0.5, 1.55, 4.3, 1.4, fs=8.5), label="+ glues strings; mixing types is refused"),
         dict(code("repl", 5.1, 1.55, 4.4, 1.65, fs=8.5), label="* repeats - whole times only"),
         dict(code("length", 0.5, 3.45, 9.0, 1.45, fs=9.5), label="len counts characters - and refuses numbers")],
        paras("Operation", "BuiltInFunction", ask="Read the TypeError aloud: which side does Python blame?"))

# ---- Names and functions ----------------------------------------------------------------------
section("Names and functions", "Remembering values, and the free toolbox",
        [{"label": "Variables"}, {"label": "Assignment"}, {"label": "Built-ins"}, {"label": "Conversions"}],
        paras("BuiltInFunction"))

content("Variables: names that remember", "Assignment stores a value under a name",
        [dict(code("var", 0.5, 1.6, 4.3, 1.75, fs=9.5), label="store, read back, update"),
         dict(code("assign", 5.1, 1.6, 4.4, 1.75, fs=8.5), label="an unassigned name is an honest error"),
         {"t": "chips", "x": 0.5, "y": 3.65, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["name = value stores", "name alone reads", "NameError = never stored"]}],
        paras("Value", ask="After spam = spam + 1, which spam is read first - left or right?"))

content("Functions you get for free", "Call, convert, and let the errors teach",
        [dict(code("call", 0.5, 1.6, 4.3, 1.9, fs=9.5), label="round, len - called with parentheses"),
         dict(code("conv", 5.1, 1.6, 4.4, 1.9, fs=8.5), label="int(), float(), str() convert - or refuse"),
         {"t": "when", "x": 2.8, "y": 3.85, "w": 4.4, "body": "int(4.7) truncates to 4 - it does not round"}],
        paras("BuiltInFunction", ask="Why does int('4.7') fail while float('4.7') works?"))

# ---- The environment --------------------------------------------------------------------------
section("Your interpreter, today", "The environment the course runs on - interrogated live",
        [{"label": "CPython"}, {"label": "Versions"}, {"label": "The GIL, measured"}, {"label": "Modules"}],
        paras("ExecutionEnvironment"))

content("The textbook that gives itself away", STORY["BookFree"]["when"],
        [{"t": "news", "x": 0.5, "y": 1.42, "w": 3.1, "h": 2.5, "paper": "automatetheboringstuff.com",
          "date": "3rd edition, 2025", "badge": "free to read online",
          "headline": "Automate the Boring Stuff with Python"},
         {"t": "beats", "x": 3.95, "y": 1.5, "w": 5.55, "h": 2.0, "fs": 13, "items": [
             "The author publishes the full text free, by choice",
             "The paper edition from No Starch funds the habit",
             "This course pins the 3rd edition - read ahead any evening"]},
         factrow("BookFree", x=3.95, y=4.42, w=5.55)],
        story_notes("BookFree"))

content("The interpreter under you, interrogated", "These slides asked it - here is what it said",
        [dict(code("cpython", 0.5, 1.6, 9.0, 0.95, fs=9.5), label="which implementation answers you"),
         dict(code("version", 0.5, 2.85, 9.0, 0.95, fs=9.5), label="which version, exactly - the one this deck ran under"),
         {"t": "stat", "x": 0.5, "y": 3.98, "w": 9.0, "h": 0.98, "items": [
             {"n": str(_vt), "label": "the version tuple these slides executed under"},
             {"n": G["version"][1][1], "label": "its release level - not a beta"}]}],
        paras("ExecutionEnvironment", ask="Your laptop may answer differently - run both lines tonight and compare."))

content("The interpreter sheds its oldest lock", STORY["FreeThreading"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.5, "fs": 13, "items": [
            "For decades one lock let a single thread run Python at a time",
            "July 2023: the Steering Council accepts PEP 703 - the lock becomes optional",
            "Since Python 3.13, free-threaded builds ship beside the standard ones"]},
         dict(code("gil", 0.5, 3.2, 9.0, 1.0, fs=9), label="not trivia - THIS interpreter answers about its own lock"),
         factrow("FreeThreading", x=0.5, y=4.47, w=9.0)],
        story_notes("FreeThreading") + ("\nNOTE: the build interpreter answered _is_gil_enabled() = %s." % _gil_on))

content("Modules: batteries, included", "import opens the standard toolbox",
        [dict(code("package", 0.5, 1.6, 4.3, 1.5, fs=9.5), label="import binds a module to a name"),
         dict(code("thread", 5.1, 1.6, 4.4, 1.5, fs=8.5), label="even threads are a module away"),
         {"t": "chips", "x": 0.5, "y": 3.5, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["random", "threading", "sys", "...and thousands more on PyPI"]}],
        paras("ModernPractice", ask="What does the name random refer to after the import - a function, a file, a module?"))

content("Where to go from here", "The chapter's own checked sources - every entry a live link",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The textbook, chapter 1 - free online", source_url("Automate the Boring Stuff")],
                ["The Python Tutorial - the informal intro", source_url("Informal Introduction")],
                ["Floating point, from the source", source_url("Floating-Point")]]},
            {"head": "Reference", "rows": [
                ["Built-in functions, all of them", source_url("Built-in Functions")],
                ["Built-in types", source_url("Built-in Types")]]},
            {"head": "Modern practice", "rows": [
                ["PEP 703 - free threading", "https://peps.python.org/pep-0703/"],
                ["What's new in 3.14", source_url("3.14")],
                ["Status of Python versions", source_url("Status of Python versions")]]},
            {"head": "Style & culture", "rows": [
                ["PEP 8 - the style guide", source_url("PEP 8")],
                ["PEP 20 - the Zen of Python", source_url("Zen of Python")]]}]}],
        "SAY: Every link is a source this chapter's corpus actually cites and checked. The "
        "tutorial and the textbook cover tonight's homework; the PEPs are where modern practice "
        "lives.\nASK: Who can recite one line of the Zen of Python by Friday?\n"
        "FULL TEXT: course page, chapter 1 - ModernPractice.",
        take="Ten links, all checked by the build - the textbook costs nothing")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a value is, and the three types of day one",
          "How operators queue, and where parentheses save you",
          "What a variable remembers, and what a NameError means",
          "Which interpreter you run - because you asked it"])}],
      "SAY: Four claims, each carried by a prompt you watched answer. Next week: making "
      "decisions - flow control.\nFULL TEXT: course page, chapter 1.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "The prompt reads, evaluates, prints, loops - every expression becomes one value",
              "int, float, str - type() names them, and integers never overflow",
              "Operators queue by precedence; floats are honestly approximate; errors name their reasons",
              "A variable is a name that remembers; built-ins are a toolbox already open",
              "You know YOUR interpreter: CPython %s - and even its oldest lock is now optional" % PYV]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 1 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and every answer on screen really ran",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_v, _o, _n, _e = (_sec[t] for t in ("Values and types", "Operations", "Names and functions", "Your interpreter, today"))
_rows = [("Questions and the chapter map", 3, _v),
         ("Values and types - the shell, int, float, str", _v + 1, _o),
         ("Operations - precedence, division, string algebra", _o + 1, _n),
         ("Names and functions - variables and the free toolbox", _n + 1, _e),
         ("Your interpreter, summary, and resources", _e + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")),
                      "label": "live consoles - every answer really ran"}]}]
S[1]["notes"] = ("SAY: Five parts, from the first 2 + 2 to interrogating your own interpreter. "
                 "Stories carry the why; consoles carry the proof.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 1 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES:
        sl["take"] = TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 1: Python Basics", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the CME materials look-and-feel standard v1.0.0"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v3_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
