#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - SEN0414 chapter 6 (Lists) at the chapter-1 standard as chapter 5 carries it (CME
materials look-and-feel v1.0.0), drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js.

Every '>>>' row comes from examples_out_v2_0_0.json (executed by examples_run_v2_0_0.py under Python 3.14) and is re-run
off the finished file by ../ch02-deck/deck_check_v1_0_1.py; every whole program is shown with its transcript and
re-verified by ../ch02-deck/program_check_v2_0_1.py. The three native charts (letters per supply name, the first six
squares, the six orders of a shuffle) are drawn ONLY from executed rows.

What differs from chapter 5's deck_build_v2_0_0.py, and why: the speaker notes follow the owner's ruling of 2026-10-08
(the decks are published and students read the notes), so every note is reader's prose in full sentences - what the
slide shows, why it matters, what to look at, one question to think about, where the full text is - with no SAY / ASK /
STORY / FULL TEXT labels; ../deck_notes_check_v1_0_0.py refuses the old form and is run on the finished file. Four
stories instead of three. The notes helper and the agenda with exact slide ranges follow SEN0401's chapter-6 deck.

Usage: python3 deck_build_v2_0_0.py   (writes deck_plan_v2_0_0.json beside itself)
       DECK_DEV=1 substitutes an available photograph for one not yet downloaded (a layout draft only, never a release)
"""
__version__ = "2.0.0"

import ast
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sys.path.insert(0, os.path.join(HERE, ".."))
C = load("corpus414_6", os.path.join(HERE, "..", "sen0414_ch06_corpus_v1_0_0.py"))
ST = load("stories414_6", os.path.join(HERE, "..", "sen0414_ch06_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch06/assets/"
DEV = os.environ.get("DECK_DEV") == "1"
PHOTO = {}
for _f in ("photo_edsger_dijkstra.jpg", "photo_ronald_fisher.jpg", "photo_magic_8_ball.jpg",
           "book_fig_000097.jpg", "book_fig_000098.jpg", "book_fig_000099.jpg", "book_fig_000100.jpg", "book_fig_000101.jpg"):
    if os.path.exists(os.path.join(HERE, ASSETS, _f)):
        PHOTO[_f] = _f
    elif DEV:
        PHOTO[_f] = "photo_edsger_dijkstra.jpg"
    else:
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v2_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]

BYNAME = {n[0]: n for n in C.NODES}
LABEL = {n[0]: (n[1] or n[0]) for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in G.values() for _, out in rows)
STORYTEXT = " ".join(s["story"] + " " + s["source"] + " " + s["when"] for s in ST.STORIES)


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def _section_of(name):
    n = BYNAME[name]
    while n[2] > 2:
        n = BYNAME[n[3]]
    return LABEL[n[0]]


CUR = [""]


def notes(*names, look=None, think=None):
    """Reader's prose for the published deck: what the slide shows (the opening sentences of the first concept's own
    explanation), what to look at, one question to think about, and where the full text is - all as sentences."""
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    CUR[0] = names[0]
    lead = BYNAME[names[0]][5][0][1]
    shows = _sentences(lead, 2)
    if len(shows) > 520:
        shows = _sentences(lead, 1)
    out = shows
    if look:
        out += " " + look.rstrip(".") + "."
    if think:
        out += " As a question to think about, consider " + think.rstrip(".?") + "."
    secs = sorted({_section_of(nm) for nm in names})
    out += " The full explanation is on the course page, chapter 6, under " + " and ".join(secs) + \
           (", in the concept" if len(names) == 1 else ", in the concepts") + " " + ", ".join(LABEL[nm] for nm in names) + "."
    return out


def story_notes(sid, look=None):
    st = STORY[sid]
    CUR[0] = st["concepts"][0]
    out = "This is a true story, dated %s. %s" % (st["when"], st["story"])
    if look:
        out += " " + look.rstrip(".") + "."
    out += " The lesson of the story, in one sentence, is this. %s. The sources are these. %s" % (st["lesson"], st["source"])
    return out


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def count_under(root):
    ids, todo = set(), [root]
    while todo:
        cur = todo.pop()
        for k in children(cur):
            if k not in ids:
                ids.add(k)
                todo.append(k)
    return len(ids)


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets" % (title, len(items)))
    for b in items:
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph" % (b, title))
    return items


def code(group, x, y, w, h, fs=12, rows=None):
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    nlines = sum(1 + (1 if out.strip() else 0) for _, out in rr)
    fit = (w - 0.4) / (maxlen * 0.0092)
    fit_h = (h - 0.30) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin (needs %.1f pt)" % (group, w, h, fs))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def prog(pname, x, y, w, h, fs=10, lines=None):
    """A chapter program, whole or an honest excerpt, with its transcript - the shape program_check_v2_0_1 verifies."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["runs"][0]["transcript"].strip()
    outlines = out.count("\n") + (1 if out else 0)
    maxlen = max(max(len(l) for l in shown), max((len(t) for t in out.split("\n")), default=0) + 8)
    nlines = len(shown) + outlines
    fit_w = (w - 0.4) / (maxlen * 0.0092)
    fit_h = (h - 0.56) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit_w, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s cannot fit unwrapped in %.1fx%.1fin (needs %.1f pt)" % (pname, w, h, fs))
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": True,
            "out": out if out else None, "outLabel": "prints",
            "cap": "program %s, lines %d to %d of %d, %s" % (pname, a, b, len(all_lines), CAP)}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + PHOTO[f], "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


BOOKCAP = "Sweigart, ATBS 3e, CC BY-NC-SA"
FIG = {"idx": "book_fig_000097.jpg", "tags": "book_fig_000098.jpg", "alias": "book_fig_000099.jpg",
       "items": "book_fig_000100.jpg", "rain": "book_fig_000101.jpg"}

# verified figures parsed back out of the executed examples: the charts are drawn from these and nothing else
_len = ast.literal_eval(G["Loop"][2][1])
assert _len == [4, 8, 13, 7], _len
_sq = ast.literal_eval(G["Mutation"][4][1])
assert _sq == [1, 4, 9, 16, 25, 36], _sq
_dev = ast.literal_eval(G["Shuffle"][-1][1])
_ord = ast.literal_eval(G["Shuffle"][-2][1])
assert len(_dev) == 6 and sum(_dev) == 0 and len(_ord) == 6, (_dev, _ord)
assert G["Alias"][3][1] == "[0, 'Hello!', 2, 3]" and G["Alias"][4][1] == "True"
assert G["Copy"][5][1] == "99" and G["Copy"][6][1] == "1", "the shallow/deep copy contrast has changed"
assert G["Mutation"][2][1] == "['b', 'd']", "the removal-while-looping trap has changed"

S = []


def slide(kind, title, sub, items, notes_text, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": bg, "concept": CUR[0]})
    CUR[0] = ""


def content(title, sub, items, notes_text, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": "light", "concept": CUR[0]}
    CUR[0] = ""
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        for it in items:
            top = it["y"] - (0.3 if it.get("t") in ("code", "prog") and it.get("label") else 0)
            if top < 1.68:
                raise SystemExit("REFUSED: %r starts at %.2f in under the lede of %r" % (it.get("label") or it.get("t"), top, title))
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes_text, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9,
              "cols": 2 if image else min(4, len(boxes)), "fs": 14, "subfs": 11, "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes_text, bg="light")


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 6: Lists", "One ordered, changeable row of values",
      [img(FIG["items"], 6.0, 1.15, 3.5, 2.12, cap="a list is one value that holds numbered items - " + BOOKCAP)],
      "This deck teaches the list, the first container of Python: one value that holds many values in order and can be "
      "changed after it is made. Every console and program on the slides was executed under Python %s, and the deck "
      "checks re-ran them on the finished file, so a result shown here is a result Python printed. The full text of every "
      "slide is on the course page for chapter 6, and the four true stories on the slides carry their sources." % PYV)

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.4, "fs": 12.5, "items": list(C.CQS)}],
        "The chapter is organised around three competency questions, and they are printed on this slide so that the reader can "
        "come back to them at the end. The first asks which list operations read, replace, add, remove, find, order and combine "
        "items, and which change the list in place. The second asks how names, copies and function arguments decide whether a "
        "change is seen elsewhere in a program. The third asks which printed outputs of the book differ in current Python and "
        "which modern forms the book leaves out. Each is answered by a range of slides in this deck, which the agenda names, and "
        "in full on the course page for chapter 6. As a question to think about, consider which of the three you could already "
        "answer from what you know about variables and strings.",
        take="If you can answer these three, chapter 6 is yours")

_branches = ("ListModel", "ChangingLists", "SearchingOrdering", "LoopsUnpacking", "SequencesReferences", "RandomPrograms")
content("One chapter, six branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.75, "w": 9.0, "h": 2.95, "cols": 3, "fs": 13, "subfs": 10.5, "accent": [4],
          "items": [{"label": LABEL[r], "sub": "%d concepts" % count_under(r)} for r in _branches]}],
        notes("ListModel", "SequencesReferences", look="The count under each branch is how many concepts the course page explains for it; the deck walks the branches in order, and the fifth, names and copies, is the one that surprises most beginners",
              think="why a chapter about a container needs a whole branch about names"),
        lede="Six branches, from what a list is to the programs it makes possible; the deck follows them in order and stops at four true stories.",
        take="Six branches - every slide today lives on this map")

# ---- Part 1: the list as a value ----------------------------------------------------------------
section("The list as a value", "Items, numbers from zero, and slices that cut out a part",
        [{"label": "A list"}, {"label": "Indexes"}, {"label": "Negative indexes"}, {"label": "Slices"}],
        notes("ListValues", "Positions", look="The picture is the book's own figure of a list and the four indexes that reach its items, which the next slides try out in a console",
              think="what a row of four lockers would have to look like for the first one to be number zero"),
        image=img(FIG["idx"], 6.4, 2.35, 3.2, 0.69, cap="a list and its indexes - " + BOOKCAP))

content("Indexes: a row of numbered lockers", "spam[0] is the first item, spam[-1] the last, and an index past the end is an error",
        [dict(code("Index", 0.5, 1.98, 5.4, 2.75), label="one list read from the front, the back, and past its end"),
         img(FIG["idx"], 6.15, 1.75, 3.35, 0.72),
         {"t": "beats", "x": 6.15, "y": 2.75, "w": 3.35, "h": 2.15, "fs": 10.5, "items": [
             "Think of a row of lockers numbered from zero: the first locker is number 0 and the last is one less than the count.",
             "A negative index counts back from the end, so spam[-1] is always the last item.",
             "An index at or past the length raises IndexError, as the last row shows."]}],
        notes("Index", "NegativeIndex", look="Read the console from the top: the first four rows reach the same list from both ends, the fifth gives the length, and the last row is the error that an index past the end raises",
              think="what spam[len(spam)] would give, and why the largest valid index is one less than the length"),
        lede="A list is a value in square brackets; each item has a number, and the numbers start at zero.",
        take="Items are numbered from zero; negative numbers count from the end")

content(STORY["ZeroStart"]["title"], STORY["ZeroStart"]["when"],
        [img("photo_edsger_dijkstra.jpg", 0.5, 1.45, 2.95, 2.02, cap="Dijkstra, 1994 - photo: A. F. Borchert, CC BY-SA 4.0"),
         {"t": "beats", "x": 3.75, "y": 1.4, "w": 5.75, "h": 1.1, "fs": 11, "items": [
             "11 August 1982: Dijkstra writes a note asking why numbering should start at zero",
             "He chooses ranges that include the start and exclude the end",
             "Then the difference of the bounds is the length, and neighbours meet without a gap"]},
         dict(code("Half", 3.75, 2.9, 5.75, 1.45), label="Python's slices keep Dijkstra's convention"),
         {"t": "when", "x": 0.5, "y": 3.95, "w": 2.95, "body": "start in, end out"},
         factrow("ZeroStart", x=0.5, y=4.66, w=9.0)],
        story_notes("ZeroStart", look="The console cuts items 2 to 5 out of a list of ten, finds that the slice has 5 minus 2 items, and shows that two neighbouring slices put together make the whole list again"))

content("Slices: a part of a list, as a new list", "list[start:stop:step] - the stop is never included",
        [dict(code("Slice", 0.5, 1.98, 5.4, 2.75), label="slices of one list: middle, front, back, every second, reversed"),
         {"t": "beats", "x": 6.15, "y": 1.85, "w": 3.35, "h": 3.0, "fs": 10.5, "items": [
             "Think of a ruler: the numbers mark the gaps between the items, and a slice takes what lies between two marks.",
             "Leaving out the start or the stop means the beginning or the end of the list.",
             "A step of -1 walks backwards, and spam[:] is a copy of the whole list.",
             "A slice is a new list, so changing it never changes the original."]}],
        notes("Slice", "SliceDefaults", "SliceStep", look="Each row of the console cuts the same four-item list differently, and the last row applies a step of three to the numbers 0 to 9, which keeps 0, 3, 6 and 9",
              think="how many items spam[1:3] holds, and how you could have known without running it"),
        lede="A slice cuts a part out of a list and returns it as a new list; its first number is included and its second is not.",
        take="A slice runs from the start up to, never including, the stop")

# ---- Part 2: changing, searching, ordering -------------------------------------------------------
content("Replace, add, remove", "One list changed in place, step by step - the same list the whole time",
        [dict(code("Change", 0.5, 1.98, 6.0, 2.75), label="six changes to one list, in order"),
         {"t": "beats", "x": 6.75, "y": 1.85, "w": 2.75, "h": 3.0, "fs": 10.5, "items": [
             "A list is like a shopping list in pencil: you may rewrite, add and cross out items.",
             "append adds at the end and insert at a chosen place.",
             "pop, del and remove all take items out; pop also hands the item back."]}],
        notes("ItemAssignment", "AppendMethod", "InsertMethod", "PopMethod", "RemoveMethod", look="After each change the console shows the list or the value returned, so the order of the rows is the order in which the list changes",
              think="which of the three ways to remove an item you would use when you know its position and which when you know its value"),
        lede="Lists are mutable: these methods change the very list they are called on and return no new list, except pop, which returns the item removed.",
        take="append, insert, pop, del and remove change the list itself")

content("Combine and search", "+ and * build new lists; in and index look for a value",
        [dict(code("Combine", 0.5, 1.98, 4.4, 2.3), label="joining and repeating lists"),
         dict(code("Search", 5.1, 1.98, 4.4, 2.3), label="looking for a value in a list"),
         {"t": "when", "x": 0.5, "y": 4.5, "w": 9.0, "body": "+ builds a new list; extend grows one; in asks whether; index asks where"}],
        notes("Concatenation", "Membership", "IndexMethod", look="On the left the plus sign gives a new list while extend changes the old one; on the right in answers True or False and index answers with a place, or with an error when the value is absent",
              think="why an expression that begins with an empty list and the word and never reaches the index that would fail"),
        lede="Plus and times make new lists, while extend and plus-equals grow an existing one; in asks whether a value is there and index asks where.",
        take="Use in to ask whether, index to ask where")

content("Order a list", "sort changes the list; sorted returns a new one",
        [dict(code("Sort", 0.5, 1.98, 5.9, 2.75), label="numbers both ways, words two ways, a mixed list fails"),
         {"t": "beats", "x": 6.65, "y": 1.85, "w": 2.85, "h": 3.0, "fs": 10.5, "items": [
             "Think of a shelf of books: sort rearranges the books on the shelf, sorted makes a sorted copy of the list of titles.",
             "Capital letters sort before small ones unless the key lowercases them.",
             "Numbers and words cannot be compared, so sorting them together fails."]}],
        notes("SortMethod", "SortKeyReverse", "SortedFunction", look="The first rows sort the numbers in place and then backwards, the next two rows show that plain sorting puts every capital letter before every small one and that the key argument repairs this, and the last row is the TypeError of a list that mixes a number and a word",
              think="when you would choose sorted over sort"),
        lede="sort rearranges the list it is called on and returns nothing; the sorted function leaves its argument alone and returns a new list.",
        take="sort changes the list; sorted gives a new one")

content(STORY["EightBall"]["title"], STORY["EightBall"]["when"],
        [img("photo_magic_8_ball.jpg", 0.5, 1.4, 1.9, 1.9, cap="'It is certain.' - photo: Zaneology, CC BY 2.0"),
         {"t": "beats", "x": 0.5, "y": 3.75, "w": 2.9, "h": 0.8, "fs": 10.5, "items": [
             "1946: Carter and Bookman invent it",
             "20 answers inside, nine in the program"]},
         prog("magic8ball_v1_0_0.py", 3.65, 1.45, 5.85, 2.9, fs=9),
         factrow("EightBall", x=0.5, y=4.66, w=9.0)],
        story_notes("EightBall", look="On the slide, the program prints three of the nine answers at random indexes, with the random seed fixed so that every run shows the same three answers"))

# ---- Part 3: loops and unpacking ----------------------------------------------------------------
section("Loops and unpacking", "Walking a list, changing it safely, and giving its items names",
        [{"label": "range and len"}, {"label": "enumerate"}, {"label": "The removal trap"}, {"label": "Starred unpacking"}],
        notes("Looping", "Unpacking", look="The picture is the book's figure of a list whose items each carry a numbered tag, which is what enumerate pairs with the items",
              think="when you need the position of an item and when the item alone is enough"),
        image=img(FIG["items"], 6.4, 2.15, 3.2, 1.94, cap="a list holds items; its indexes are labels on them - " + BOOKCAP))

content("Loop over a list", "Item by item, or with the number beside each item",
        [dict(code("Loop", 0.5, 1.98, 6.3, 2.2), label="enumerate pairs; a comprehension builds a new list"),
         {"t": "chart", "x": 7.0, "y": 1.75, "w": 2.5, "h": 2.75, "ctype": "bar",
          "title": "Letters per name",
          "dataLabels": True, "dlFmt": "0", "dlFs": 10,
          "labels": ["pens", "staplers", "flamethrowers", "binders"],
          "series": [{"name": "letters", "data": _len}]},
         {"t": "when", "x": 0.5, "y": 4.5, "w": 6.3, "body": "enumerate when you need the numbers"}],
        notes("EnumerateLoop", "RangeLenLoop", "ListComprehension", look="The bars are computed, not typed: the second console row is the list of lengths [4, 8, 13, 7] that gives their heights, and the first row shows the pairs that enumerate produces",
              think="why enumerate is usually clearer than a loop over range(len(supplies))"),
        lede="A for loop visits the items in order; enumerate adds each item's number, and a comprehension turns a loop into a new list.",
        take="Loop over the items; ask enumerate when you also need the numbers")

content("Never remove from the list you loop over", "Like taking chairs out of a row while you count along it",
        [dict(code("Mutation", 0.5, 1.98, 5.3, 2.75), label="the loop skips items; a comprehension is safe"),
         {"t": "chart", "x": 6.0, "y": 1.75, "w": 3.5, "h": 2.2, "ctype": "bar",
          "title": "The first six squares, from a comprehension",
          "dataLabels": True, "dlFmt": "0", "dlFs": 10,
          "labels": ["1", "2", "3", "4", "5", "6"],
          "series": [{"name": "square", "data": _sq}]},
         {"t": "when", "x": 6.0, "y": 4.15, "w": 3.5, "body": "build a new list instead"}],
        notes("MutationWhileIterating", "ListComprehension", look="The loop meant to remove all four letters removes only two and leaves b and d, because each removal moves the next item into the place the loop has just passed; the bars below the console show what a comprehension builds without touching the source",
              think="what the loop would have left if the list had held six letters"),
        lede="The loop meant to empty the list leaves two items behind, because the numbering shifts under it after every removal.",
        take="Change a copy or build a new list; never edit what you are looping over")

content("Unpacking: names for the items", "One assignment, several names - and a star that takes the rest",
        [dict(code("Unpack", 0.5, 1.98, 5.6, 2.75), label="names, a starred name, a swap, a wrong count"),
         {"t": "beats", "x": 6.35, "y": 1.85, "w": 3.15, "h": 3.0, "fs": 10.5, "items": [
             "Think of sorting a parcel into labelled pigeonholes: one item for each name.",
             "The star name takes every item the others leave, as a list.",
             "a, b = b, a swaps two values without a helper variable.",
             "With too few or too many names Python raises ValueError."]}],
        notes("MultipleAssignment", "StarredUnpacking", look="The first two rows give three names to three items; the starred row gives first one item and rest the other three; the swap exchanges two values; and the last row is the ValueError of a count that does not match",
              think="how many items a starred name receives when the list has exactly as many items as the other names"),
        lede="Unpacking assigns each item of a list to its own name in one statement; one starred name may collect the remaining items.",
        take="Match names to items, or star one name to take the rest")

# ---- Part 4: names, references, copies -----------------------------------------------------------
section("Names and copies", "A list is one thing with many possible name tags",
        [{"label": "Mutable and immutable"}, {"label": "Aliasing"}, {"label": "Arguments"}, {"label": "Shallow and deep"}],
        notes("References", "SequenceTypes", look="The picture is the book's figure of a number with a name tag and then two tags, which shows that assignment attaches a tag to a value and does not copy the value",
              think="what the third panel of the picture says happens to the old value when spam receives a new one"),
        image=img(FIG["tags"], 6.4, 2.15, 3.2, 1.13, cap="a name is a tag on a value - " + BOOKCAP))

content("Two names, one list", "eggs = spam copies the tag, not the list - and a function receives the same list",
        [dict(code("Alias", 0.5, 1.98, 5.4, 2.75), label="a change seen through two names, and through a parameter"),
         img(FIG["alias"], 6.1, 1.75, 3.4, 1.07, cap="the book's figure of two tags on one list"),
         {"t": "beats", "x": 6.1, "y": 3.25, "w": 3.4, "h": 1.65, "fs": 10.5, "items": [
             "Think of two keys to one locker: opening it with either shows the same contents.",
             "A function that changes its list parameter changes the caller's list."]}],
        notes("Aliasing", "ListArguments", look="After eggs receives the new item spam shows it too and the is operator confirms that both names point at one list; the last four rows show that a function which appends to its parameter changes the list the caller passed",
              think="what a program must do when it needs to change a list without the caller seeing the change"),
        lede="Assigning a list to another name attaches a second tag to the same list, so a change through either name is seen through both.",
        take="Assignment copies the name, not the list")

content("Copies: shallow and deep", "A list of lists needs a deep copy - and [[0] * 3] * 2 is the classic trap",
        [dict(code("Copy", 0.5, 1.98, 5.6, 2.75), label="a shallow copy shares the inner lists; deepcopy does not"),
         {"t": "beats", "x": 6.35, "y": 1.85, "w": 3.15, "h": 3.0, "fs": 10.5, "items": [
             "Think of photocopying a folder: a shallow copy copies the folder, but the pages inside are still the originals.",
             "copy.deepcopy copies the pages too, however deeply they are nested.",
             "Repeating a list of lists with * repeats the reference, so every row is the same row."]}],
        notes("ShallowCopy", "DeepCopy", "ReplicationAliasing", look="After the first change the shallow copy shows 99 in the inner list it shares with the original, while the deep copy still shows 1; the last three rows show that two rows made by repetition change together",
              think="how you would build a grid of three rows of three zeros that does not share its rows"),
        lede="A shallow copy duplicates only the outer list, so the inner lists are shared with the original; a deep copy duplicates every level.",
        take="Copy nested lists with deepcopy, and never repeat them with *")

# ---- Part 5: random choices and programs --------------------------------------------------------
content(STORY["Shuffle"]["title"], STORY["Shuffle"]["when"],
        [img("photo_ronald_fisher.jpg", 0.5, 1.45, 2.0, 2.38, cap="Fisher, 1952 - B. Eagel, CC BY-SA 4.0"),
         {"t": "beats", "x": 3.0, "y": 1.45, "w": 6.5, "h": 1.0, "fs": 11, "items": [
             "1938: Fisher and Yates print a pencil-and-paper shuffle",
             "1964: Durstenfeld's computer version, still behind random.shuffle",
             "Fair: every order equally likely, so about 1000 each in 6000 deals"]},
         dict(code("Shuffle", 3.0, 2.78, 4.4, 1.65), label="six thousand shuffles of three cards"),
         {"t": "chart", "x": 7.45, "y": 2.45, "w": 2.05, "h": 2.1, "ctype": "bar",
          "title": "Deals above or below 1000",
          "dataLabels": True, "dlFmt": "0", "dlFs": 8,
          "labels": _ord,
          "series": [{"name": "deals above or below 1000", "data": _dev}]},
         factrow("Shuffle", x=0.5, y=4.66, w=9.0)],
        story_notes("Shuffle", look="The console deals three cards six thousand times, counts how often each of the six possible orders appears and subtracts the expected one thousand; the largest difference is %d deals in six thousand, which is what a fair shuffle gives, and the bars show the six differences" % max(abs(d) for d in _dev)))

content(STORY["DigitalRain"]["title"], STORY["DigitalRain"]["when"],
        [img(FIG["rain"], 0.5, 1.45, 3.4, 2.06, cap="the screensaver program run in a console - " + BOOKCAP),
         {"t": "beats", "x": 0.5, "y": 3.85, "w": 3.4, "h": 0.7, "fs": 10, "items": [
             "1999: film glyphs by Simon Whiteley",
             "The screensaver is a list of counters"]},
         prog("matrix_v1_0_0.py", 4.1, 1.45, 5.4, 2.9, fs=9),
         factrow("DigitalRain", x=0.5, y=4.66, w=9.0)],
        story_notes("DigitalRain", look="The program keeps one counter per column in a list: a counter above zero prints a random digit and counts down, and a counter at zero prints a space, so streams of digits start and end on their own"))

content("Comma Code: a list into a sentence", "One function, four lists - including the two awkward short ones",
        [prog("commacode_v1_0_0.py", 0.5, 1.98, 5.9, 2.7, fs=10),
         {"t": "beats", "x": 6.65, "y": 1.85, "w": 2.85, "h": 3.0, "fs": 10.5, "items": [
             "Think of reading a shopping list aloud: commas between the items and an 'and' before the last.",
             "items[:-1] slices off the last item, and items[-1] is that item.",
             "Fewer than three items need no commas at all."]}],
        notes("CommaCode", "Slice", look="The function joins everything but the last item with commas and then adds the word and and the last item; the four transcripts show the usual case, the two-item case, the one-item case and the empty list",
              think="which of the four test lists would fail if the function always put a comma before the and"),
        lede="A slice and a join turn any list into an English phrase; the program is tested on four lists, including the empty one.",
        take="Slices and join turn a list into a sentence")

content("Coin Flip Streaks: a simulation with lists", "10,000 experiments of 100 flips each - how often does six in a row appear?",
        [prog("coinstreaks_v1_0_0.py", 0.5, 1.98, 6.0, 2.85, fs=9.5),
         {"t": "beats", "x": 6.75, "y": 1.85, "w": 2.75, "h": 3.0, "fs": 10.5, "items": [
             "Think of flipping a coin until your arm tires: most people expect six in a row to be rare.",
             "Each experiment is a list of 100 random choices of H or T.",
             "The estimate, about 81 in 100, shows that long streaks are normal."]}],
        notes("CoinFlipStreaks", "RandomChoice", look="Each pass of the outer loop makes one list of a hundred flips and the inner loop walks along it, extending the current run when two neighbours are equal and restarting it otherwise; the single line printed is the percentage of experiments whose longest run reached six",
              think="why the fixed random seed matters if you want to compare two versions of the program"),
        lede="The program flips a coin 100 times, looks for a run of six equal results in the list, and repeats the experiment 10,000 times.",
        take="A list of random choices lets you measure what intuition guesses")

# ---- summary, resources, closing ------------------------------------------------------------------
content("The chapter in five lines", "One line per part - each one provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A list is one value holding many items in order; its numbers start at zero, negative numbers count from the end, and a slice returns a new list",
            "A list changes in place: assign, append, insert, pop, del, remove; sort orders it, and sorted returns an ordered copy",
            "Loop over the items, ask enumerate for the numbers, never remove from the list you are looping over, and unpack items into names",
            "Assignment copies a name, not a list: two names can reach one list, a function can change its caller's list, and nested lists need deepcopy",
            "random.choice and random.shuffle make lists the heart of programs: an eight ball, a screensaver, a comma sentence and a simulation"]}],
        "These five lines are the deck in miniature, one per part, and each of them is carried by a range of slides that the "
        "agenda names. A line that feels unproven should send the reader back to its consoles, because every result in it was "
        "executed. The full text behind all five lines is on the course page for chapter 6.",
        take="If a line feels unproven, its part's slides carry the receipt")

content("Where to go from here", "Checked 2026-10-08; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["This chapter, free online", "https://automatetheboringstuff.com/3e/chapter6.html"],
                ["Python tutorial: data structures", "https://docs.python.org/3/tutorial/datastructures.html"],
                ["Sorting Techniques - the official HOWTO", "https://docs.python.org/3/howto/sorting.html"]]},
            {"head": "Standards and documentation", "rows": [
                ["copy - shallow and deep copy operations", "https://docs.python.org/3/library/copy.html"],
                ["PEP 3132 - extended iterable unpacking", "https://peps.python.org/pep-3132/"],
                ["random - pseudo-random numbers", "https://docs.python.org/3/library/random.html"]]},
            {"head": "Watch and try", "rows": [
                ["Facts and myths about Python names and values", "https://nedbatchelder.com/text/names.html"],
                ["Python Tutor - draw your list and its names", "https://pythontutor.com/"]]},
            {"head": "The stories", "rows": [
                ["Dijkstra, why numbering should start at zero", "https://www.cs.utexas.edu/~EWD/transcriptions/EWD08xx/EWD831.html"],
                ["The Fisher-Yates shuffle", "https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle"]]}]}],
        "Everything here is free to read, and every link was opened on the date in the subtitle. A good exercise is to paste "
        "the aliasing console of this deck into Python Tutor and watch the two name tags arrive on one list, and then to read "
        "the official sorting guide for the key argument. The course page for chapter 6 carries the full resource list with "
        "a sentence on why each entry is there.",
        take="Draw your lists in Python Tutor and watch the names")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a list holds, and how indexes and slices reach it",
          "Which methods change a list in place and which return a new one",
          "Why two names can reach one list, and when a program must copy",
          "How a list drives an eight ball, a screensaver and a simulation"])}],
      "Four claims, each carried by consoles and programs that ran on a slide of this deck. The course page for chapter 6 "
      "carries every word behind them, the four stories with their sources, and the question bank to test the four claims "
      "on yourself.", bg="dark")

# ---- agenda -----------------------------------------------------------------------------------
S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Six parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Six parts - and at the end, programs you can read line by line",
             "bg": "light"})
_idx = {s["title"]: i + 1 for i, s in enumerate(S)}          # slide number = position + 1 after the insert below
_n = len(S)
_first = lambda t: _idx[t]
_a = _first("The list as a value")
_b = _first("Replace, add, remove")
_c = _first("Loops and unpacking")
_d = _first("Names and copies")
_e = _first(STORY["Shuffle"]["title"])
_f = _first("The chapter in five lines")
_rows = [("Questions and the chapter map", 3, _a - 1),
         ("The list as a value - indexes, Dijkstra, slices", _a, _b - 1),
         ("Changing, combining, searching, ordering - and the eight ball", _b, _c - 1),
         ("Loops and unpacking - the removal trap", _c, _d - 1),
         ("Names and copies - aliasing, deep copies", _d, _e - 1),
         ("Random choices and programs - shuffle, rain, comma code, coin flips", _e, _f - 1),
         ("Summary, resources and what you can now say", _f, _n)]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.4, "h": 3.4, "fs": 12, "items": [
                      ("%s  (slide %d)" if _x == _y else "%s  (slides %d-%d)") % ((_ti, _x) if _x == _y else (_ti, _x, _y)) for _ti, _x, _y in _rows]},
                 {"t": "stat", "x": 7.15, "y": 1.5, "w": 2.35, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))),
                      "label": "consoles and programs, each with its result"}]}]
S[1]["notes"] = ("The route has six parts and ends with programs that the reader can follow line by line. One story is a note "
                 "that a Dutch computer scientist wrote in 1982 about starting to count at zero, one is the fair shuffle of "
                 "1938 and 1964, one is a toy that answers questions from a list of twenty replies, and one is the green rain "
                 "of a famous film. The part a reader expects to be hardest is names and copies, and it is worth marking now and "
                 "checking again at the summary slide.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for line in str(s["notes"]).splitlines():
        if re.match(r"^\s*(?:[A-Z][A-Z \-/&()0-9]{1,24}|say|ask|tell|show|story|cue|demo|note|full text|read|point|click|pause|transition|timing)\s*(?:\([^)]*\))?\s*:", line):
            raise SystemExit("REFUSED: slide %r carries a directive label in its notes: %r" % (s["title"], line[:60]))
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
_story_titles = {STORY[k]["title"] for k in STORY}
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl and sl["title"] not in _story_titles]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides, the standard is 20-26" % len(S))

plan = {"meta": {"title": "Chapter 6: Lists", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-08, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0), notes as reader's prose"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
