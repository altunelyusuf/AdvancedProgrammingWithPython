#!/usr/bin/env python3
"""Builds deck_plan_v4_0_0.json - SEN0414 chapter 3 (Loops and Modules) on the CME classroom standard.

Same regime as chapter 1 (CME materials look-and-feel v1.0.0, the shared renderer, the >>> chip):
numbered warm-ivory slides, agenda with exact ranges, summary before live-linked resources, word
gates, 5N1K stories with fact rows, consoles WITH results and errors as Python raised them. New
here: whole PROGRAMS with their transcripts - each panel captioned 'program <name>, lines a to b
of n', re-executed and text-verified off the finished file by program_check_v2_0_0.py, while
deck_check_v1_0_1.py re-runs every '>>>' row.

Usage: python3 deck_build_v3_0_0.py   (writes deck_plan_v3_0_0.json beside itself)
"""
__version__ = "4.0.0"

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


C = load("corpus414_3", os.path.join(HERE, "..", "sen0414_ch03_corpus_v1_0_0.py"))
ST = load("stories414_3", os.path.join(HERE, "..", "sen0414_ch03_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch03/assets/"
for _f in ("photo_carl_gauss.jpg", "photo_edsger_dijkstra.jpg"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v2_1_0.json")))
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
    out += "\nFULL TEXT: course page, chapter 3 - " + ", ".join(names) + "."
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
    'The questions this chapter answers': 'If you can answer these, chapter 3 is yours',
    'One chapter, five branches': 'Five branches - every slide today lives on this map',
    'The schoolboy who refused to loop': 'A loop is honest work - and sometimes a formula beats it',
    'while repeats; for visits': 'while guards a condition; for walks a collection',
    'Why range(5) stops before five': 'Half-open ranges are a 1982 argument your loops obey',
    'range: start, stop, step - lazily': 'range describes numbers without building them',
    'Lists, tuples, dicts - the things loops visit': 'Three containers, three jobs - and one for loop fits all',
    'enumerate and zip: positions and pairs': 'Stop counting by hand - Python hands you the index',
    'break, continue - and loops inside loops': 'break leaves the innermost loop; label your exits with functions',
    'The 1997 twister inside random': 'import random wakes a named, dated, published algorithm',
    'import: one line, a whole toolbox': 'A module is a namespace you choose to open',
    'When imports and loops go wrong': 'Read the last line first - Python names its reasons',
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
slide("title", "Chapter 3: Loops and Modules", "Doing it again until it is done - and importing what others finished",
      [{"t": "code", "x": 6.0, "y": 1.3, "w": 3.5, "h": 1.7, "fs": 12, "cap": CAP,
        "rows": [["sum(range(101))", "5050"], ["list(range(3))", "[0, 1, 2]"]]}],
      "SAY: Chapter 2 chose between paths; chapter 3 repeats them: while and for, the "
      "containers loops visit, and the modules that save you writing loops at all.\n"
      "FULL TEXT: course page, chapter 3.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.1, "fs": 12.5,
          "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["every answer ran", "whole programs with transcripts", "sources on the last slide"]}],
        paras("Repetition"))

content("One chapter, five branches", "The concept map the whole chapter hangs on",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 12, "root": "Chapter 3",
          "nodes": [{"label": decamel(r), "kids": [decamel(x) for x in children(r, 2)[:7]]}
                    for r in ("Repetition", "Sequence", "LoopControl", "Module", "ModernPractice")]}],
        paras("Repetition", "Module"),
        lede="Each branch is a question the chapter answers; the grey lists are the concepts that answer it, every one explained on the course page.")

# ---- Repeating --------------------------------------------------------------------------------
section("Repeating", "while guards; for visits; range describes",
        [{"label": "while"}, {"label": "for"}, {"label": "range"}, {"label": "Accumulators"}],
        paras("Repetition"))

content("The schoolboy who refused to loop", STORY["GaussSum"]["when"],
        [img("photo_carl_gauss.jpg", 0.5, 1.45, 2.6, 3.0, cap="Gauss, by Jensen (1840) - public domain"),
         {"t": "beats", "x": 3.5, "y": 1.5, "w": 6.0, "h": 1.5, "fs": 12.5, "items": [
             "Add 1 to 100, said the teacher; fifty pairs of 101, said the boy",
             "A legend with a paper trail - first printed 1856, versions traced since"]},
         dict(prog("gauss_v1_0_0.py", 3.5, 3.1, 6.0, 1.3, fs=9), label="the loop earns 5050; the formula agrees without looping"),
         factrow("GaussSum", x=0.5, y=4.55, w=9.0)],
        story_notes("GaussSum"))

content("while repeats; for visits", "The same five greetings, two machines",
        [dict(prog("fivetimes_while_v1_0_0.py", 0.5, 1.55, 4.3, 2.9, fs=8), label="while: you manage the counter"),
         dict(prog("fivetimes_for_v1_0_0.py", 5.1, 1.55, 4.4, 2.9, fs=8), label="for: range hands you each i"),
         {"t": "when", "x": 2.8, "y": 4.6, "w": 4.4, "body": "same transcript, different bookkeeping"}],
        paras("Repetition", ask="Which version can forget to advance - and what happens then?"))

content("Why range(5) stops before five", STORY["ZeroStart"]["when"],
        [img("photo_edsger_dijkstra.jpg", 0.5, 1.45, 2.4, 2.9, cap="Dijkstra - photo: Hamilton Richards, CC BY-SA 3.0"),
         {"t": "beats", "x": 3.3, "y": 1.5, "w": 6.2, "h": 1.5, "fs": 12.5, "items": [
             "A handwritten 1982 memo: include the start, exclude the stop",
             "Lengths become stop minus start; adjacent ranges meet without overlap"]},
         dict(code("halfopen", 3.3, 3.08, 6.2, 1.34, fs=8.5), label="the memo's promise, kept by range"),
         factrow("ZeroStart", x=0.5, y=4.55, w=9.0)],
        story_notes("ZeroStart"))

content("range: start, stop, step - lazily", "A description of numbers, not a box of them",
        [dict(code("rangess", 0.5, 1.6, 4.3, 1.3, fs=9.5), label="start and stop"),
         dict(code("rangestep", 5.1, 1.58, 4.4, 1.34, fs=9.5), label="the step, forwards and down"),
         dict(code("lazyrange", 0.5, 3.3, 4.3, 1.55, fs=9), label="a billion numbers, no memory - laziness measured"),
         dict(code("accumulate", 5.1, 3.3, 4.4, 1.55, fs=9), label="the accumulator pattern every total uses")],
        paras("Repetition", "Sequence", ask="Why does range(10**9) cost nothing until you loop it?"))

# ---- Sequences --------------------------------------------------------------------------------
section("Sequences", "What for loops visit",
        [{"label": "Lists"}, {"label": "Tuples and dicts"}, {"label": "enumerate / zip"}, {"label": "Unpacking"}],
        paras("Sequence"))

content("Lists, tuples, dicts - the things loops visit", "Three containers, one loop",
        [dict(code("listval", 0.5, 1.6, 4.3, 1.9, fs=9), label="lists: ordered, changeable"),
         dict(code("dictval", 5.1, 1.6, 4.4, 1.3, fs=8.5), label="dicts: loop keys, values, or pairs"),
         dict(prog("dict_ops_v1_0_0.py", 5.1, 3.16, 4.4, 1.1, fs=9), label="a dict grows and counts"),
         {"t": "chips", "x": 0.5, "y": 3.75, "w": 4.3, "h": 0.95, "fs": 11.5,
          "items": ["list: [ ] mutable", "tuple: ( ) fixed", "dict: { } key to value"]}],
        paras("Sequence", ask="Which of the three would hold the days of the week - and why that one?"))

content("enumerate and zip: positions and pairs", "Stop counting by hand",
        [dict(code("enumerate", 0.5, 1.6, 9.0, 1.3, fs=9.5), label="enumerate hands you index and item together"),
         dict(prog("for_pairs_v1_0_0.py", 0.5, 3.2, 4.3, 1.3, fs=9), label="the loop, whole"),
         dict(code("zipstrict", 5.1, 3.2, 4.4, 1.3, fs=8.5), label="zip pairs two sequences - strict= catches ragged ones")],
        paras("Sequence", "ModernPractice", ask="What does zip do with unequal lengths without strict=True?"))

# ---- Loop control -----------------------------------------------------------------------------
section("Loop control", "Leaving early, skipping, and nesting",
        [{"label": "break"}, {"label": "continue"}, {"label": "Nested loops"}, {"label": "Iterators"}],
        paras("LoopControl"))

content("break, continue - and loops inside loops", "The exits, demonstrated",
        [dict(prog("break3_v1_0_0.py", 0.5, 1.55, 4.3, 1.75, fs=9), label="break: out of the innermost loop"),
         dict(prog("nested_break_v1_0_0.py", 5.1, 1.55, 4.4, 1.75, fs=9), label="nested: the outer loop carries on"),
         dict(prog("iter_next_v1_0_0.py", 0.5, 3.6, 4.3, 1.35, fs=9), label="under every for: iter and next"),
         dict(code("ctrlgroup", 5.1, 3.6, 4.4, 1.35, fs=9), label="continue skips; else rewards a clean finish")],
        paras("LoopControl", ask="Rewrite the nested break to leave BOTH loops - what tool does chapter 4 offer?"))

# ---- Modules ----------------------------------------------------------------------------------
section("Modules", "Importing what others finished",
        [{"label": "import"}, {"label": "The standard library"}, {"label": "random"}, {"label": "Namespaces"}],
        paras("Module"))

content("The 1997 twister inside random", STORY["MersenneRandom"]["when"],
        [{"t": "beats", "x": 0.5, "y": 1.45, "w": 9.0, "h": 1.45, "fs": 13, "items": [
            "Matsumoto and Nishimura, 1997-98: the Mersenne Twister",
            "Period 2^19937 - 1: the sequence outlives any lifetime",
            "Python's default generator - and the docs say: not for cryptography"]},
         dict(code("randmod", 0.5, 3.05, 9.0, 1.1, fs=9), label="the module answers, deterministically where it can"),
         factrow("MersenneRandom", x=0.5, y=4.47, w=9.0)],
        story_notes("MersenneRandom"))

content("import: one line, a whole toolbox", "Modules are namespaces you choose to open",
        [dict(code("modgroup", 0.5, 1.6, 4.3, 1.5, fs=9), label="import, then dot into it"),
         dict(code("namespace", 5.1, 1.6, 4.4, 1.5, fs=8.5), label="the names stay inside the module"),
         dict(code("stdlib", 0.5, 3.5, 9.0, 1.3, fs=9.5), label="batteries included: the standard library, sampled")],
        paras("Module", ask="Why does the course never write from module import * ? (the next slide shows)"))

content("When imports and loops go wrong", "Honest failures, read aloud",
        [dict(code("importerr", 0.5, 1.6, 9.0, 1.25, fs=9.5), label="ModuleNotFoundError: the name, exactly"),
         dict(code("starnames", 0.5, 3.15, 4.3, 1.5, fs=9), label="import * pollutes - counted"),
         dict(code("exceptions", 5.1, 3.15, 4.4, 1.7, fs=8), label="the loop-era errors, in one place")],
        paras("Module", "LoopControl", ask="Which error here is a TYPO, which a MISSING INSTALL - and how do you tell?"))

content("Where to go from here", "The chapter's own checked sources - every entry a live link",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The textbook, chapter 3 - free online", source_url("Automate the Boring Stuff")],
                ["The tutorial: for, range, loop else", source_url("More Control Flow")]]},
            {"head": "Reference", "rows": [
                ["Compound statements (for, while)", source_url("Compound statements")],
                ["Built-in types: sequences and dicts", source_url("Built-in Types")],
                ["The random module", source_url("random")]]},
            {"head": "History", "rows": [
                ["EWD831 - why numbering starts at zero", "https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html"],
                ["The Mersenne Twister", "https://en.wikipedia.org/wiki/Mersenne_Twister"]]},
            {"head": "Style", "rows": [
                ["PEP 8 on imports", source_url("PEP 8")]]}]}],
        "SAY: Every link is a source the chapter corpus cites and checked. Read EWD831 tonight - "
        "two handwritten pages, and range() never confuses you again.\n"
        "ASK: Find the stdlib module that already solves your current side project.\n"
        "FULL TEXT: course page, chapter 3 - Module.",
        take="Eight links, all checked by the build - Dijkstra's memo is two pages")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "When while fits and when for does",
          "What range describes, and why it stops early",
          "How enumerate and zip remove hand-counting",
          "What import gives you, and what it protects"])}],
      "SAY: Four claims, each carried by a transcript you watched print. Next week: functions - "
      "naming the loops you just wrote.\nFULL TEXT: course page, chapter 3.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "while guards a condition; for visits a collection - same transcript, different bookkeeping",
              "range describes numbers lazily, half-open since Dijkstra's 1982 memo",
              "Lists change, tuples do not, dicts map - and one for loop serves all three",
              "break leaves the innermost loop; enumerate and zip end hand-counting",
              "import opens a namespace: the 1997 Mersenne Twister answers your randint"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 3 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and every transcript on screen really printed",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("Repeating", "Sequences", "Loop control", "Modules"))
_rows = [("Questions and the chapter map", 3, _a),
         ("Repeating - while, for, range", _a + 1, _b),
         ("Sequences - lists, dicts, enumerate, zip", _b + 1, _c),
         ("Loop control - break, continue, nesting", _c + 1, _d),
         ("Modules, summary, and resources", _d + 1, len(S))]
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
S[1]["notes"] = ("SAY: Five parts, from Gauss's shortcut to the twister inside random - every "
                 "transcript verified off this very file.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 3 - every section.")

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

plan = {"meta": {"title": "Chapter 3: Loops and Modules", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the CME materials look-and-feel standard v1.0.0"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v4_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
