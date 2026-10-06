#!/usr/bin/env python3
"""Builds deck_plan_v3_0_0.json - SEN0414 chapter 2 (Flow Control) on the CME classroom standard.

Same regime as chapter 1 (CME materials look-and-feel v1.0.0, the shared renderer, the >>> chip):
numbered warm-ivory slides, agenda with exact ranges, summary before live-linked resources, word
gates, 5N1K stories with fact rows, consoles WITH results and errors as Python raised them. New
here: whole PROGRAMS with their transcripts - each panel captioned 'program <name>, lines a to b
of n', re-executed and text-verified off the finished file by program_check_v2_0_0.py, while
deck_check_v1_0_1.py re-runs every '>>>' row.

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


C = load("corpus414_2", os.path.join(HERE, "..", "sen0414_ch02_corpus_v1_0_0.py"))
ST = load("stories414_2", os.path.join(HERE, "..", "sen0414_ch02_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch02/assets/"
for _f in ("photo_george_boole.jpg",):
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
    out += "\nFULL TEXT: course page, chapter 2 - " + ", ".join(names) + "."
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
    'The questions this chapter answers': 'If you can answer these, chapter 2 is yours',
    'One chapter, seven branches': 'Seven branches - every slide today lives on this map',
    'The man inside the bool type': "Every if statement runs on one Victorian's algebra",
    'Two values rule everything': 'bool is a type like any other - with only two citizens',
    'and, or, not - and who gets lazy': 'Short-circuiting is a feature you will deliberately use',
    'The whitespace that is the syntax': 'In Python the layout cannot lie about the logic',
    'if, else - and the block that belongs': 'The colon opens a block; the indent owns it',
    'elif: the ladder with one exit': 'One ladder, one rung taken - order decides',
    'A thirty-year-old wish, granted in 3.10': 'match is a 2021 feature - you saw it arrive',
    'match: patterns, captures, guards': 'A pattern can destructure and bind, not just compare',
    'The walrus: test and keep in one move': 'Assign inside the expression - sparingly, by style',
    'Three errors you will actually meet': 'Read the last line first - Python names its reasons',
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
slide("title", "Chapter 2: Flow Control", "Booleans, branches, and the programs that finally make decisions",
      [{"t": "code", "x": 6.0, "y": 1.3, "w": 3.5, "h": 1.7, "fs": 12, "cap": CAP,
        "rows": [["2 + 2 == 4", "True"], ["bool('')", "False"]]}],
      "SAY: Chapter 1 computed values; chapter 2 lets programs choose between them. Today: the "
      "two-valued algebra, the if family, and the 2021 match statement.\n"
      "FULL TEXT: course page, chapter 2.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.9, "fs": 13,
          "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["every answer ran", "whole programs with transcripts", "errors are answers too"]}],
        paras("FlowControl"))

content("One chapter, seven branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 4, "fs": 12.5, "subfs": 10, "accent": [3],
          "items": [{"label": decamel(r), "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("Value", "Comparison", "BooleanOperation", "FlowControl", "WorkedProgram", "ErrorReport", "ModernPractice")]}],
        paras("FlowControl", "BooleanOperation"),
        lede="Seven branches; the count under each is how many concepts the course page explains for it - today walks the spine.")

# ---- Booleans and truthiness ------------------------------------------------------------------
section("Booleans and truthiness", "The two-valued algebra under every decision",
        [{"label": "bool"}, {"label": "Truthiness"}, {"label": "Comparisons"}, {"label": "Chaining"}],
        paras("Value"))

content("The man inside the bool type", STORY["BooleTruth"]["when"],
        [img("photo_george_boole.jpg", 0.5, 1.45, 2.7, 3.1, cap="George Boole - public domain, via Wikimedia Commons"),
         {"t": "beats", "x": 3.6, "y": 1.5, "w": 5.9, "h": 2.3, "fs": 13, "items": [
             "A shoemaker's son from Lincoln, self-taught",
             "1847 and 1854: reasoning itself obeys algebra",
             "He never saw a computer; every circuit runs his logic",
             "Python's True-and-False type carries his name: bool"]},
         factrow("BooleTruth", x=3.6, y=4.05, w=5.9)],
        story_notes("BooleTruth"))

content("Two values rule everything", "bool, and the comparisons that produce it",
        [dict(code("boolean", 0.5, 1.55, 4.3, 1.62, fs=9.5), label="a type with two citizens"),
         dict(code("eqgroup", 5.1, 1.55, 4.4, 1.62, fs=9.5), label="== asks; = stores - the classic mix-up, refused"),
         dict(code("chained", 0.5, 3.45, 9.0, 1.45, fs=9.5), label="comparisons chain like mathematics - 18 < age < 65 just works")],
        paras("Value", "Comparison", ask="Why is 1 == 1.0 True but '1' == 1 False?"))

content("Truthiness: what counts as something", "Every value answers bool() - emptiness answers False",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Zero, empty text, empty containers: falsy",
            "Everything else: truthy",
            "So 'if name:' reads as 'if name is not empty'"]},
         dict(code("truthgroup", 4.3, 1.55, 5.2, 1.5, fs=9.5), label="the census, run"),
         dict(code("emptiness", 0.5, 3.52, 9.0, 1.38, fs=9.5), label="the idiom the style guide prefers")],
        paras("Value", ask="When would 'if x:' and 'if x != 0:' disagree? (think containers)"))

# ---- Combining conditions ---------------------------------------------------------------------
section("Combining conditions", "and, or, not - Boole's three operations",
        [{"label": "and / or"}, {"label": "not"}, {"label": "Short-circuit"}, {"label": "Precedence"}],
        paras("BooleanOperation"))

content("and, or, not - and who gets lazy", "Short-circuiting, shown misbehaving on purpose",
        [dict(code("logicgroup", 0.5, 1.6, 4.3, 1.5, fs=9.5), label="the truth tables, sampled"),
         dict(code("shortcirc", 5.1, 1.6, 4.4, 1.9, fs=8.5), label="the right side may never run - even a 1/0 survives"),
         dict(prog("shortcircuit_v1_0_0.py", 0.5, 3.58, 9.0, 1.38, fs=9), label="the program version: the guard runs first, so the crash never comes")],
        paras("BooleanOperation", ask="Rewrite 'x != 0 and 10 / x > 1' with the operands swapped - what changes?"))

# ---- Branching --------------------------------------------------------------------------------
section("Branching", "The if family, and the indentation that owns it",
        [{"label": "if / else"}, {"label": "Indentation"}, {"label": "elif ladders"}, {"label": "Nesting"}],
        paras("FlowControl"))

content("The whitespace that is the syntax", STORY["IndentationChoice"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.45, "w": 9.0, "h": 1.0, "fs": 12.5, "items": [
            "Same five lines, one space of difference - and two different programs",
            "A lesson carried from the ABC language: what you see is what the interpreter sees"]},
         dict(prog("indent_in_v1_0_0.py", 0.5, 2.6, 4.3, 1.75, fs=9), label="'always' inside the block"),
         dict(prog("indent_out_v1_0_0.py", 5.1, 2.6, 4.4, 1.75, fs=9), label="'always' outside - it prints"),
         factrow("IndentationChoice", x=0.5, y=4.55, w=9.0)],
        story_notes("IndentationChoice"))

content("if, else - and the block that belongs", "The chapter's password program, whole",
        [{"t": "numlist", "x": 0.5, "y": 1.55, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "The condition ends in a colon; the block indents",
            "else answers the same condition's No",
            "Blocks nest: the inner if runs only inside the outer Yes"]},
         dict(prog("password_v1_0_0.py", 4.3, 1.55, 5.2, 2.6, fs=9), label="nested decisions, and both prints that follow"),
         {"t": "when", "x": 0.5, "y": 3.75, "w": 3.55, "body": "colon opens; indent owns"}],
        paras("FlowControl", ask="Move 'Access granted.' one level left - what changes in the transcript?"))

content("elif: the ladder with one exit", "Order decides which rung fires",
        [dict(prog("littlekid_v1_0_0.py", 0.5, 1.55, 4.3, 2.5, fs=9), label="the ladder takes exactly one rung"),
         dict(prog("vampire_v1_0_0.py", 5.1, 1.55, 4.4, 2.9, fs=8), label="conditions may combine and, or, not"),
         {"t": "chips", "x": 0.5, "y": 4.35, "w": 4.3, "h": 0.55, "fs": 12,
          "items": ["first true wins", "else = none did"]}],
        paras("FlowControl", ask="Swap the first two rungs of the ladder - which inputs now answer differently?"))

# ---- Patterns, style and errors ----------------------------------------------------------------
section("Patterns, style, errors", "The 2021 match statement, the walrus, and honest failures",
        [{"label": "match"}, {"label": "Guards and captures"}, {"label": "The walrus"}, {"label": "Error reports"}],
        paras("ModernPractice"))

content("A thirty-year-old wish, granted in 3.10", STORY["MatchArrives"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.42, "w": 9.0, "h": 1.25, "fs": 12.5, "items": [
            "'Where is my switch?' - answered for decades with elif chains",
            "February 2021: the Steering Council accepts PEPs 634-636",
            "October 2021: Python 3.10 ships match - patterns that destructure and bind"]},
         dict(prog("match_command_v1_0_0.py", 0.5, 2.78, 9.0, 1.7, fs=8.5), label="the first match: command words, one case wins"),
         factrow("MatchArrives", x=0.5, y=4.56, w=9.0)],
        story_notes("MatchArrives"))

content("match: patterns, captures, guards", "More than a switch - the pattern binds what it matches",
        [dict(prog("match_guard_v1_0_0.py", 0.5, 1.55, 5.6, 2.3, fs=9), label="a guard refines the pattern; the capture is a real name"),
         {"t": "numlist", "x": 6.4, "y": 1.6, "w": 3.1, "h": 1.9, "fs": 10.5, "items": [
            "case (x, y) destructures a pair",
            "if x == y guards the case",
            "the bound names outlive the match"]},
         {"t": "chips", "x": 0.5, "y": 4.1, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["literal patterns", "capture patterns", "sequence patterns", "guards"]}],
        paras("FlowControl", "ModernPractice", ask="Which elif ladder from earlier would you rewrite as a match - and which not?"))

content("The walrus: test and keep in one move", "PEP 572's := - assignment inside the expression",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Alone, x := 3 is a SyntaxError on purpose",
            "Inside a condition it assigns AND tests",
            "Style: use it where it removes a duplicate call"]},
         dict(code("walrus", 4.3, 1.6, 5.2, 1.6, fs=9), label="the operator, probed at its edges"),
         dict(prog("walrus_size_v1_0_0.py", 0.5, 3.7, 9.0, 1.15, fs=9.5), label="the honest use: compute once, test, reuse")],
        paras("ModernPractice", ask="Why does the bare x := 3 refuse while (x := 3) works?"))

content("Three errors you will actually meet", "Read them as answers, not accidents",
        [dict(code("nameerr", 0.5, 1.55, 4.3, 1.3, fs=9), label="NameError: the name was never stored"),
         dict(code("typeerr", 5.1, 1.55, 4.4, 1.3, fs=8.5), label="TypeError: right operation, wrong types"),
         dict(code("zerodiv", 0.5, 3.15, 4.3, 1.3, fs=9), label="ZeroDivisionError - floats included"),
         dict(code("syntaxerr", 5.1, 3.15, 4.4, 1.3, fs=8.5), label="SyntaxError: refused before running at all")],
        paras("ErrorReport", ask="Which of the four can an if statement guard against - and which cannot?"))

content("Where to go from here", "The chapter's own checked sources - every entry a live link",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The textbook, chapter 2 - free online", source_url("Automate the Boring Stuff")],
                ["The tutorial: more control flow", source_url("More Control Flow")]]},
            {"head": "Reference", "rows": [
                ["Truth testing and booleans", source_url("Built-in Types")],
                ["Compound statements (if, match)", source_url("Compound statements")]]},
            {"head": "Modern practice", "rows": [
                ["PEP 636 - match, by tutorial", "https://peps.python.org/pep-0636/"],
                ["PEP 572 - the walrus operator", source_url("PEP 572")]]},
            {"head": "Style", "rows": [
                ["PEP 8 on comparisons and booleans", source_url("PEP 8")]]}]}],
        "SAY: Every link is a source the chapter corpus cites and checked. PEP 636 is the "
        "gentlest tutorial ever attached to a PEP - read it with tonight's homework.\n"
        "ASK: Find the PEP 8 rule these slides obeyed every time they tested emptiness.\n"
        "FULL TEXT: course page, chapter 2 - ModernPractice.",
        take="Eight links, all checked by the build - the match tutorial reads in one coffee")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What bool is, and what truthiness buys",
          "How and, or, not combine - and when they stay lazy",
          "Why indentation IS the block, with two programs as proof",
          "When an elif ladder should become a match"])}],
      "SAY: Four claims, each carried by a program whose transcript you watched. Next week: "
      "loops - doing it again until it is done.\nFULL TEXT: course page, chapter 2.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "bool has two citizens; comparisons mint them, and emptiness counts as False",
              "and, or, not follow Boole's algebra - and evaluate only as far as they must",
              "The indentation IS the block: two five-line programs proved the one-space difference",
              "if, elif, else take exactly one path; match (3.10) destructures, binds and guards",
              "Errors are answers: NameError, TypeError, ZeroDivisionError, SyntaxError - read the last line first"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 2 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and every transcript on screen really printed",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("Booleans and truthiness", "Combining conditions", "Branching", "Patterns, style, errors"))
_rows = [("Questions and the chapter map", 3, _a),
         ("Booleans and truthiness - the two-valued algebra", _a + 1, _b),
         ("Combining conditions - and, or, not, laziness", _b + 1, _c),
         ("Branching - if, elif, and the indentation", _c + 1, _d),
         ("Patterns, style, errors, summary, resources", _d + 1, len(S))]
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
S[1]["notes"] = ("SAY: Five parts, from Boole's algebra to honest errors - with whole programs and "
                 "their transcripts verified off this very file.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 2 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES and TAKES[sl["title"]]:
        sl["take"] = TAKES[sl["title"]]
EXTRA = {
    'Truthiness: what counts as something': 'Emptiness is False; if name: is idiomatic Python',
}
for sl in S:
    if sl["kind"] == "content" and "take" not in sl and EXTRA.get(sl["title"]):
        sl["take"] = EXTRA[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 2: Flow Control", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the CME materials look-and-feel standard v1.0.0"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v3_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
