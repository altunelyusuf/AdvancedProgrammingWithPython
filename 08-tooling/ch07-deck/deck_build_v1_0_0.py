#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 7 (Dictionaries and Structuring Data) on the CME classroom standard.

Same regime as chapters 1 to 5: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows and credited photographs, consoles and whole programs
with their results as Python printed them. Every console result, program transcript, chart value and table cell comes
from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py); the speaker notes are prose for the reader.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"
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


C = load("corpus414_7", os.path.join(HERE, "..", "sen0414_ch07_corpus_v1_0_0.py"))
ST = load("stories414_7", os.path.join(HERE, "..", "sen0414_ch07_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch07/assets/"
IMG = json.load(open(os.path.join(HERE, "..", "ch07-page", "stories_img_v1_0_0.json")))
RES = json.load(open(os.path.join(HERE, "..", "ch07-page", "resources_v1_1_0.json")))["links"]
for _k, _v in IMG.items():
    if not _k.startswith("_"):
        for _f in _v:
            if not os.path.exists(os.path.join(HERE, ASSETS, _f["file"])):
                raise SystemExit("REFUSED: missing asset %s" % _f["file"])
if not os.path.exists(os.path.join(HERE, ASSETS, "book_fig_000103.jpg")):
    raise SystemExit("REFUSED: missing book figure")
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CH = EX["_charts"]
TB = EX["_tables"]
LEAD = {n[0]: n[5][0][1] for n in C.NODES}


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in" % (group, w))
    h = round(lines_of(rr) * fs * 1.32 / 72.0 + 0.36, 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.083:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def prog(pname, x, y, w, fs=8, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'),
    as program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    maxlen = max(max(len(l) for l in shown), max((len(t) for t in out.split("\n")), default=0) + 8)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, w, fs))
    h = round((len(shown) + outlines) * fs * 1.32 / 72.0 + 0.40, 2)
    label = "program %s, lines %d to %d of %d - Python %s" % (pname, a, b, len(all_lines), PYV)
    if len(label) > (w - 0.1) / 0.083:
        label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: caption %r is too long for a %.1f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, h, fs=9, label="what the run printed"):
    """The transcript of a program beside its code: a panel holding only the lines the run printed."""
    out = PROGS[pname]["transcript"]
    fs = min(fs, round((w - 0.4) / ((max(len(t) for t in out.split("\n")) + 7) * 0.0088), 1))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": out,
            "outLabel": "prints", "label": label}


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body, x, y, w, h, fs=11.5, accent=None):
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


S = []


def content(title, sub, items, notes, take, lede=None):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 7: Dictionaries",
          "sub": "Dictionaries and Structuring Data: pairs, counts, models and the text that carries them",
          "items": [{"t": "code", "x": 6.0, "y": 0.9, "w": 3.5, "h": 0.8, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Chapters 1 to 6 worked with single values and with lists, where a position names an item. This chapter "
                   "introduces the dictionary, where a name of your own choosing names an item, and then uses it to count "
                   "letters, to group words, to model a chessboard and to write data down as text. Every example on these "
                   "slides was run under Python 3.14.6 and the result printed beside it is the result Python gave.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) ---------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Five parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Five parts, from one pair to a chessboard, all of it executed.",
          "bg": "light"})

# ---- 3 questions -----------------------------------------------------------------------------------------------------
_branches = [n for n in C.NODES if n[2] == 1]


def _count(root):
    ids, out = {root}, 0
    for n in C.NODES:
        if n[3] in ids:
            ids.add(n[0]); out += 1
    return out


content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.35, "w": 9.0, "h": 2.95, "fs": 11.5, "items": list(C.CQS)},
         {"t": "chips", "x": 0.5, "y": 4.38, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["%d branches" % len(_branches), "%d concepts" % len(C.NODES), "%d examples" % sum(1 for n in C.NODES if n[4]),
                    "Python %s" % PYV]}],
        "These five questions are the checklist for the chapter. The first asks what you can do to the pairs of a dictionary, the "
        "second asks what may serve as a key, the third asks how counting, grouping and nesting are solved, the fourth asks how "
        "a real thing is modelled and written down, and the fifth is about vocabulary. The chips below them give the "
        "size of the chapter: its branches, the concepts the course page explains, the worked examples and the Python they ran on. "
        "The summary slide answers every question in one line.",
        "Answer these five questions and you have the chapter.")

# ---- 4 the dictionary data type --------------------------------------------------------------------------------------
c, bot = con("basic", 0.5, 1.5, 5.6, fs=11, label="a dictionary is written in braces, and a key finds its value")
content("The dictionary data type", "A collection of key-value pairs, looked up by key",
        [c,
         {"t": "bullets", "x": 0.5, "y": bot + 0.12, "w": 5.6, "h": 4.95 - bot - 0.12, "fs": 11.5, "items": [
             "Each pair joins a key to a value with a colon; the pairs sit in braces.",
             "A key finds its value directly, however many pairs the dictionary holds.",
             "Since Python 3.7 a dictionary also remembers the order in which keys were added."]},
         card("A phone book", "The name is the key and the number beside it is the value. You look a person up by name and "
              "never ask which page they are on, and you do not care which entry was written first.",
              6.4, 1.5, 3.1, 3.3, fs=12)],
        "A dictionary stores pairs. The key is the part you look things up by, and the value is the part you want back. In the "
        "console on this slide the keys are the words size, color and disposition, and my_cat['size'] returns the value that "
        "was stored with the key size. A phone book is the everyday picture: you search by name, the name stands for the "
        "number, and the order in which people were added is not how you find them. The last bullet matters because older "
        "teaching, including the printed chapter, says a dictionary has no order, whereas every current Python keeps insertion order.",
        "A dictionary finds a value by its key, not by its position.")

# ---- 5 dictionaries versus lists -------------------------------------------------------------------------------------
c, bot = con("versus", 5.1, 1.78, 4.4, fs=10, label="lists compare by order, dictionaries do not", cap=False)
content("Dictionaries versus lists", "Two containers, two ways to name an item",
        [{"t": "compare", "x": 0.5, "y": 1.5, "w": 4.3, "h": 3.4, "fs": 11.5,
          "left": {"head": "A list", "rows": ["Items are named by position: 0, 1, 2.",
                                              "Two lists are equal only if the items come in the same order.",
                                              "Use it for a sequence: the days of a week."]},
          "right": {"head": "A dictionary", "rows": ["Items are named by a key you choose.",
                                                     "Two dictionaries are equal if they hold the same pairs, in any order.",
                                                     "Use it for a lookup: a birthday for each name."]}},
         c,
         card("Equal, yet remembered", "eggs == ham is True, and list(ham) still shows the order of insertion.",
              5.1, bot + 0.1, 4.4, 4.95 - bot - 0.1, fs=11)],
        "The comparison on the left is the difference to remember. A list is a row of boxes numbered from zero, so moving an item "
        "changes the list. A dictionary is a set of labelled drawers, so the same drawers in another order are still the same "
        "dictionary. The console on the right shows both facts: the two lists are not equal because their order differs, the two "
        "dictionaries are equal although their pairs were written in a different order, and the keys of the second one still "
        "come out in the order in which they were added.",
        "Dictionaries with the same pairs are equal, in any order.")

# ---- 6 story: dictionary order ---------------------------------------------------------------------------------------
_im = IMG["DictOrderRuling"][0]
content("Five words that gave dictionaries an order", STORY["DictOrderRuling"]["when"],
        [img(_im["file"], 0.5, 1.45, 3.6, 2.4, cap=_im["credit"]),
         {"t": "beats", "x": 4.4, "y": 1.5, "w": 5.1, "h": 2.7, "fs": 12, "items": [
             "Python 3.6 (2016): a compact dictionary happens to keep insertion order",
             "It was a detail of CPython, not a promise of the language",
             "15 December 2017: Guido van Rossum writes 'Make it so.'",
             "From Python 3.7 the language guarantees insertion order"]},
         factrow("DictOrderRuling")],
        story_notes("DictOrderRuling"),
        "One ruling made insertion order part of the language.")

# ---- 7 keys must be hashable -----------------------------------------------------------------------------------------
c, bot = con("keys", 0.5, 1.5, 9.0, fs=11, label="a tuple is accepted as a key, a list is refused, and 1, 1.0 and True collide", cap=True)
content("Keys must be hashable", "A key has to be a value that never changes",
        [c,
         {"t": "boxes", "x": 0.5, "y": bot + 0.1, "w": 9.0, "h": 4.95 - bot - 0.1, "cols": 3, "fs": 12, "subfs": 10, "accent": [],
          "items": [{"label": "Hashable", "sub": "int, float, str, bool, and tuples of these"},
                    {"label": "Not hashable", "sub": "list, dict and set can change"},
                    {"label": "One key, three spellings", "sub": "1, 1.0 and True are equal"}]}],
        "A dictionary finds a key by computing a number from it, called its hash, and that number is only trustworthy if the key "
        "can never change. This is why a tuple works as a key and a list does not. Python 3.14 words the error as cannot use "
        "list as a dict key, and older versions said unhashable type list, so the wording on your machine may differ while "
        "the rule stays the same. The last console row shows a quirk: because 1, 1.0 and True are equal and hash alike, the "
        "dictionary keeps a single key, the first one written, and the last value assigned to it.",
        "Keys must never change, and 1, 1.0 and True are one key.")

# ---- 8 reading a key -------------------------------------------------------------------------------------------------
c, bot = con("read", 0.5, 1.5, 5.6, fs=10.5, label="in, get(), a missing key, and setdefault()")
content("Reading a key", "Test first, ask with a fallback, or add only if missing",
        [c,
         card("A coat-check ticket", "Hand over a ticket you were given and you get your coat. A ticket never issued gets you "
              "a refusal, which is a KeyError. get() is the attendant who answers 'none' instead of refusing, and "
              "setdefault() hangs a new coat up when the ticket is new.", 6.4, 1.5, 3.1, 3.4, fs=11.5)],
        "There are three ways to read a key that might not be there. The in operator asks whether the key exists and gives True or "
        "False. The get method returns the value or a default you supply, and it leaves the dictionary unchanged, so the 'eggs' "
        "lookup returns 0 and adds nothing. Square brackets raise a KeyError for a missing key, which you see in the console as "
        "KeyError: 'eggs', and setdefault stores a value only when the key is missing, then returns whatever the dictionary now "
        "holds for that key. The last row proves that setdefault changed the dictionary and get did not.",
        "Use get() when a missing key is normal.")

# ---- 9 changing pairs ------------------------------------------------------------------------------------------------
c, bot = con("change", 0.5, 1.5, 5.4, fs=11, label="assign to add or replace, del and pop to remove, | to merge")
content("Changing pairs", "Add, replace, remove and merge",
        [c,
         card("What each line did", "spam['name'] = ... added a pair. del removed the age pair, and a missing key would raise a "
              "KeyError. pop() removed color and handed its value back. The | operator built a new dictionary from two, and "
              "where both have a key the right-hand value wins; spam itself did not change.",
              6.2, 1.5, 3.3, 3.45, fs=11.5)],
        "Assigning to a key does two jobs: it adds the pair if the key is new and replaces the value if the key already exists. "
        "The del statement and the pop method remove a pair, and pop also returns the value, which is handy when you want to "
        "use what you remove. Since Python 3.9 the | operator merges two dictionaries into a new one in which the right-hand "
        "side wins on a shared key, and |= does the same in place. The last row, dict.fromkeys, builds a dictionary from a "
        "list of keys with one starting value.",
        "Assignment adds or replaces, pop removes, and | merges.")

# ---- 10 birthdays ----------------------------------------------------------------------------------------------------
p1, bot = prog("birthdays_v1_0_0.py", 0.5, 1.5, 5.0, fs=9, show_out=False)
p2 = transcript("birthdays_v1_0_0.py", 5.6, 1.5, 3.9, p1["h"], fs=9, label="typed: Alice, Eve, Dec 5, Eve")
content("A program that remembers: birthdays", "The in test chooses between a lookup and a new pair",
        [p1, p2,
         {"t": "text", "x": 0.5, "y": bot + 0.15, "w": 9.0, "h": 4.95 - bot - 0.15, "fs": 12,
          "body": "An unknown name is asked for its birthday and stored, so the next lookup of the same name succeeds."}],
        "This is the chapter's first whole program. The dictionary holds a birthday for each name, the in operator decides "
        "whether the name is known, and an unknown name is added with an assignment so that the next lookup succeeds. In the run on "
        "the right the typed names were Alice, Eve, Dec 5 and Eve, followed by an empty line that ends the loop. Eve was "
        "unknown the first time, so the program asked for her birthday and stored it, and the second time it answered "
        "from the dictionary. The data lives only as long as the program does, which is the reason for the last part of "
        "the chapter on writing data down.",
        "One in test and one assignment make a program that learns.")

# ---- 11 views and loops ----------------------------------------------------------------------------------------------
p1, bot = prog("loops_v1_0_0.py", 0.5, 1.5, 6.3, fs=8.5)
content("Views and loops", "items() unpacks pairs, and keys() is a view that sees later changes",
        [p1,
         card("A shop window", "A view is a window onto the shop, not a photograph of it. When the shelf changes, "
              "the window changes. A list() or sorted() is the photograph.", 7.0, 1.5, 2.5, 3.0, fs=11),
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 6.3, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "for k, v in d.items() gives each pair; sorted(d) is a new sorted list of keys; reversed(d) walks the newest key first."}],
        "Looping over a dictionary gives its keys, and the methods keys, values and items give views of the keys, the values and "
        "the pairs. A view is live: the program takes spam.keys() before adding the key name, and printing the view afterwards "
        "still shows name, because the view looks at the dictionary and not at a snapshot. When you want a snapshot, or a "
        "sorted order, wrap the view in list() or call sorted() on the dictionary. Python 3.8 added reversed() for dictionaries, "
        "which is why the last line prints the newest key first.",
        "A view follows the dictionary; list() and sorted() freeze it.")

# ---- 12 counting characters ------------------------------------------------------------------------------------------
p1, bot = prog("charcount_short_v1_0_0.py", 0.5, 1.5, 6.1, fs=7.5)
ch = CH["letters"]
content("Counting characters", "setdefault() starts each count at 0, then one is added per character",
        [p1,
         {"t": "chart", "x": 6.7, "y": 1.5, "w": 2.8, "h": 3.2, "ctype": "bar", "dataLabels": True, "dlFs": 9,
          "title": "Eight most common characters",
          "labels": ch["labels"], "series": [{"name": "count", "data": ch["values"]}]},
         {"t": "text", "x": 0.5, "y": bot + 0.08, "w": 6.1, "h": 4.95 - bot - 0.08, "fs": 11,
          "body": "Tally marks on paper: one stroke per sighting, one row per character, and the chart shows the longest rows."}],
        "Counting is the dictionary pattern you will use most. The key is the thing being counted, here a character, and the "
        "value is how many times it has been seen. The setdefault call makes sure the key exists with a count of zero, and "
        "the next line adds one. The program prints three counts that the chapter's output also shows, and then the "
        "number of different characters, 23, against the 73 characters of the message. The chart beside the code takes its "
        "eight tallest bars from the same message, counted by a Counter, and the space is the most common character.",
        "Counting by key turns any text into a table of totals.")

# ---- 13 story: bright cold day ---------------------------------------------------------------------------------------
_im = IMG["BrightColdDay"][0]
content("The sentence the character counter counts", STORY["BrightColdDay"]["when"],
        [img(_im["file"], 0.5, 1.4, 2.0, 2.5),
         {"t": "text", "x": 2.9, "y": 3.95, "w": 6.6, "h": 0.3, "fs": 9, "italic": True, "color": "mute", "body": "Photo: " + _im["credit"]},
         {"t": "beats", "x": 2.9, "y": 1.5, "w": 6.6, "h": 2.4, "fs": 12, "items": [
             "The message in the program is the first sentence of Nineteen Eighty-Four",
             "Secker and Warburg published the novel in London on 8 June 1949",
             "Counted by the program: 73 characters, 23 of them different",
             "Thirteen spaces and three letters c, from the same table"]},
         factrow("BrightColdDay")],
        story_notes("BrightColdDay"),
        "The lines that count one sentence count a whole novel.")

# ---- 14 Counter, defaultdict and grouping ----------------------------------------------------------------------------
p1, bot = prog("grouping_v1_0_0.py", 0.5, 1.8, 6.3, fs=7.5)
c, cb = con("counter", 6.9, 1.8, 2.6, fs=9, label="Counter counts in one call")
content("Counter, defaultdict and grouping", "setdefault() or defaultdict(list) groups words; Counter counts in one call",
        [c, p1,
         {"t": "text", "x": 0.5, "y": bot + 0.1, "w": 9.0, "h": 4.95 - bot - 0.1, "fs": 11.5,
          "body": "Pigeonholes: each word is slipped into the hole for its first letter, and a new hole appears when needed."}],
        "Two tools from the collections module remove the setdefault line. A Counter takes any iterable and returns a "
        "dictionary of counts, and its most_common method lists the biggest first. A missing key in a Counter reads as 0 "
        "instead of raising an error. The grouping program on the right solves a related problem, sorting words into lists by "
        "first letter, first with setdefault and then with a defaultdict, and its last line prints True because the two "
        "dictionaries are equal. Pigeonholes are the picture: each word goes into the hole labelled with its first letter.",
        "Counter counts, defaultdict groups, both create missing keys.")

# ---- 15 modelling ----------------------------------------------------------------------------------------------------
c, bot = con("model", 0.5, 1.8, 5.5, fs=10, label="Figure 7-2's board as a dictionary")
content("Modelling a real thing", "A chessboard becomes a dictionary",
        [c,
         img("book_fig_000103.jpg", 6.3, 1.4, 2.9, 3.0, cap="Sweigart (2025), Figure 7-2: the board that the dictionary describes"),
         {"t": "text", "x": 0.5, "y": bot + 0.1, "w": 5.5, "h": 4.95 - bot - 0.1, "fs": 11.5,
          "body": "A square is a key such as 'c6'; the piece is the value, a colour letter and a piece letter."}],
        "To model a real thing you decide what the keys and the values are. For a chessboard the book uses the name of a square, "
        "such as c6, as the key and a two-letter piece, such as wQ for a white queen, as the value. Only occupied squares "
        "are stored, so an empty square is simply a key that is absent, which the console shows with board.get('a1', 'empty'). "
        "The figure is Figure 7-2 of Sweigart's chapter, used for teaching with its credit, and it shows the five pieces "
        "that the dictionary on the left describes.",
        "A good model stores only what is there.")

# ---- 16 story: chess notation ----------------------------------------------------------------------------------------
_im = IMG["ChessNotation"][0]
content("The squares a1 to h8 are three centuries old", STORY["ChessNotation"]["when"],
        [img(_im["file"], 0.5, 1.45, 3.6, 2.36, cap=_im["credit"]),
         {"t": "beats", "x": 4.4, "y": 1.5, "w": 5.1, "h": 2.7, "fs": 12, "items": [
             "1730s: Philipp Stamma devises an early form of algebraic notation",
             "1847: Howard Staunton describes the system in his handbook",
             "1981: FIDE stops recognising descriptive notation",
             "The program's keys 'a1' to 'h8' reuse that notation"]},
         factrow("ChessNotation")],
        story_notes("ChessNotation"),
        "The best keys are often a notation people already use.")

# ---- 17 the board as a table -----------------------------------------------------------------------------------------
_tb = TB["board"]["rows"]
_occupied = sum(1 for r in _tb[1:] for cell in r[1:] if cell)
content("The board as a table", "The starting position, drawn from the dictionary",
        [{"t": "table", "x": 0.5, "y": 1.45, "w": 5.4, "rows": _tb, "colW": [0.4] + [0.625] * 8, "fs": 11, "rowH": 0.37},
         {"t": "stat", "x": 6.3, "y": 1.45, "w": 3.2, "h": 2.0, "vert": True, "items": [
             {"n": str(_occupied), "label": "squares hold a piece, so 32 keys"},
             {"n": str(64 - _occupied), "label": "squares have no key at all"}]},
         card("A seating chart", "It lists only the seats that someone occupies. Nobody writes 'empty' 32 times.",
              6.3, 3.6, 3.2, 1.3, fs=11)],
        "The table is not typed in; it was produced by looking up each of the 64 square names in the starting-position "
        "dictionary, and an empty cell means the lookup found no key. Of the 64 squares 32 hold a piece, so the dictionary has "
        "32 keys and the other 32 squares do not appear in it. The dictionary is the model, and the table is only one way of "
        "displaying it, which is the point of keeping the data separate from the printing function. The book's program draws "
        "this same board as text in a terminal window.",
        "The dictionary is the data; the table is one view of it.")

# ---- 18 chess commands -----------------------------------------------------------------------------------------------
p1, _ = prog("chessMoves_v1_0_0.py", 0.5, 1.5, 9.0, fs=7.8)
content("Chess commands are dictionary operations", "Every command of the simulator is one or two operations on the board",
        [p1],
        "The chapter's simulator accepts the commands move, remove, set, reset, clear and quit, and each one is a single "
        "dictionary operation or two. A move copies the piece to the new key and then deletes the old key, remove deletes "
        "a key, set assigns one, reset replaces the board with a copy of the starting position, and clear empties it. This "
        "short program drives the same operations without the text board so that you can see each effect in the printed "
        "list of keys. The copy in the reset line is important and it is the subject of slide 20.",
        "Moving a piece is copy-then-delete.")

# ---- 19 nested dictionaries ------------------------------------------------------------------------------------------
p1, _ = prog("guestpicnic_v1_0_0.py", 0.5, 1.5, 9.0, fs=7.6)
content("Nested dictionaries: the picnic", "Dictionaries inside a dictionary hold records inside a record",
        [p1],
        "A guest list is a dictionary of dictionaries: each guest is a key, and each guest's value is another dictionary of items "
        "and quantities. The function total_brought walks the guests and uses get with a default of zero, so a guest who brings "
        "none of an item simply adds nothing. The printed totals are 7 apples, 3 cups, no cakes, 3 ham sandwiches and 1 apple "
        "pie. A filing cabinet is the picture, with a folder for each guest and a sheet inside it for each kind of food.",
        "get() with a default keeps the picnic totals honest.")

# ---- 20 copying ------------------------------------------------------------------------------------------------------
p1, bot = prog("copying_v1_0_0.py", 0.5, 1.5, 9.0, fs=8)
content("Copying: alias, shallow and deep", "Changing an inner dictionary shows which copies share it",
        [p1,
         {"t": "boxes", "x": 0.5, "y": bot + 0.1, "w": 9.0, "h": 4.97 - bot - 0.1, "cols": 3, "fs": 11, "subfs": 9.5, "accent": [],
          "items": [{"label": "Alias", "sub": "two names for one person"},
                    {"label": "Shallow copy", "sub": "shortcuts to the same files"},
                    {"label": "Deep copy", "sub": "a full photocopy of everything"}]}],
        "Three lines make three different things. The assignment alias = original creates no copy, it only gives the same "
        "dictionary a second name. The call copy.copy builds a new outer dictionary whose inner dictionaries are still the same "
        "objects, so changing an inner value is seen through the shallow copy, while copy.deepcopy copies every level. After "
        "the program changes an inner value to 99, the alias and the shallow copy print 99 and the deep copy still prints 5, "
        "and the last line prints True False, because the shallow copy shares the inner dictionary and the deep copy does not.",
        "A shallow copy shares inner dictionaries; deepcopy does not.")

# ---- 21 writing data down --------------------------------------------------------------------------------------------
c1, b1 = con("notation", 0.5, 1.75, 4.6, fs=8, label="json, pprint and TypedDict in a console", cap=True)
p1, b2 = prog("matching_v1_0_0.py", 5.3, 1.75, 4.2, fs=8)
content("Writing data down and checking its shape", "Text, tidy printing, typed records and patterns",
        [c1, p1,
         {"t": "text", "x": 5.3, "y": b2 + 0.15, "w": 4.2, "h": 4.95 - b2 - 0.15, "fs": 11.5,
          "body": "The first case needs both keys and an age above 5; otherwise the second case matches."},
         {"t": "text", "x": 0.5, "y": b1 + 0.1, "w": 4.6, "h": 4.95 - b1 - 0.1, "fs": 11.5,
          "body": "TypedDict is checked by type checkers only: at run time Cat(...) is a plain dict."}],
        "A dictionary vanishes when the program ends, so it has to be turned into text to be saved or sent. The json module's dumps "
        "turns a dictionary into JSON text and loads turns it back, and pprint.pformat lays a big dictionary out tidily, with its "
        "keys sorted. The TypedDict describes which keys a record must have, but Python does not enforce it when "
        "the program runs, as the last row shows with its plain dict, and only a type checker complains. The match statement on "
        "the right tests a dictionary against a pattern and binds the values it finds, so the first case needs both keys and "
        "an age above 5.",
        "JSON carries a dictionary out of a program.")

# ---- 22 story: JSON --------------------------------------------------------------------------------------------------
_im = IMG["JsonBirth"][0]
content("The notation that carries dictionaries", STORY["JsonBirth"]["when"],
        [img(_im["file"], 0.5, 1.45, 3.6, 2.38, cap=_im["credit"]),
         {"t": "beats", "x": 4.4, "y": 1.5, "w": 5.1, "h": 2.7, "fs": 12, "items": [
             "April 2001: Crockford and Morningstar send the first JSON message",
             "December 2005: Yahoo offers some web services in JSON",
             "13 December 2017: the IETF publishes JSON as RFC 8259",
             "Python's json module converts a dictionary to that text and back"]},
         factrow("JsonBirth")],
        story_notes("JsonBirth"),
        "JSON is how a dictionary leaves a program and comes back.")

# ---- 23 practice -----------------------------------------------------------------------------------------------------
p1, _ = prog("inventory_v1_0_0.py", 0.5, 1.5, 6.1, fs=7, show_out=False)
p2 = transcript("inventory_v1_0_0.py", 6.75, 1.5, 2.75, p1["h"], fs=9)
content("Practice: the fantasy game inventory", "Display a dictionary of items, then add the dragon's loot to it",
        [p1, p2],
        "The practice project of the chapter stores a player's items as a dictionary from the item name to the count. The first "
        "function prints each item and the total, which is 62 for the starting stuff, and the second function adds a list of "
        "loot to an inventory, using setdefault so that a new item starts at zero. The loot list repeats gold coin three times, "
        "so the inventory ends with 45 gold coins, since it started with 42, and 48 items in all. The chessboard validator "
        "project is on the course page, in the practice section.",
        "Each practice program reads a dictionary and applies a rule.")

# ---- 24 summary ------------------------------------------------------------------------------------------------------
content("The chapter in five lines", "One line for each question the chapter set",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "fs": 12, "items": [
            "Assign to add or replace a pair, and use del or pop to remove one, with get() when a missing key is normal.",
            "A key must be hashable, so a tuple is welcome and a list is not, and dictionaries have kept insertion order since 3.7.",
            "Counting and grouping take setdefault, Counter or defaultdict, and a view follows the dictionary while list() freezes it.",
            "A chessboard is a dictionary of occupied squares, and a nested dictionary holds a record inside a record.",
            "copy.copy shares the inner dictionaries, deepcopy does not, and JSON writes the data down as text."]}],
        "These five lines answer the five questions of slide 3, one each. The first line covers the operations on pairs, the second "
        "covers the rules for keys and the changes between the printed chapter and today's Python, and the third covers counting, "
        "grouping and views. The fourth is about modelling and nesting, and the fifth is about copying and writing data down. If a line "
        "feels unproven, the part of the route that carries it has the slides with the executed examples.",
        "If a line feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(" - ")[0] if r["kind"] != "book" else "The textbook, chapter 7 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": rows(("book",)) + rows(("discussion",))[:0] + [
                ["Python tutorial: data structures", "https://docs.python.org/3/tutorial/datastructures.html"],
                ["Built-in types: dict and its views", "https://docs.python.org/3/library/stdtypes.html"]]},
            {"head": "Libraries", "rows": [
                ["collections: Counter and defaultdict", "https://docs.python.org/3/library/collections.html"],
                ["copy: shallow and deep copies", "https://docs.python.org/3/library/copy.html"],
                ["json and pprint", "https://docs.python.org/3/library/json.html"]]},
            {"head": "History", "rows": [
                ["Guido's ruling on dictionary order, 2017", "https://mail.python.org/pipermail/python-dev/2017-December/151283.html"],
                ["PEP 584: merge operators for dict", "https://peps.python.org/pep-0584/"],
                ["RFC 8259: the JSON standard", "https://datatracker.ietf.org/doc/html/rfc8259"]]},
            {"head": "Watch and try", "rows": [
                ["Modern Dictionaries, Raymond Hettinger", "https://www.youtube.com/watch?v=p33CVV29OG8"],
                ["Python Tutor: step through your code", "https://pythontutor.com/"]]}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read online and has the "
        "chessboard and picnic programs, and the documentation links lead to the exact module of each library used today. "
        "The history links are for the curious: the python-dev message is the ruling that gave dictionaries their order, and the "
        "video is a talk by the core developer who proposed the compact layout. Python Tutor lets you step through a program "
        "and watch a dictionary change, which is the best way to understand the copying slide.",
        "Eleven links, each opened on the day this deck was built.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.55, "w": 8.8, "h": 2.0, "fs": 17, "items": [
            "A dictionary finds values by key, and keys must be hashable.",
            "Counting and grouping are three lines with setdefault, or one with Counter.",
            "A real thing becomes a dictionary of the parts that are there.",
            "A shallow copy shares the inner dictionaries, and JSON writes the data down."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d console rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples "
        "yourself, you have the chapter. The next chapter moves on to strings and text editing.",
        "Questions are welcome; bring one example you could not predict.")

# ---- agenda ----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The dictionary type and its keys", "The questions this chapter answers", "Changing pairs"),
          ("Loops, counting and grouping", "A program that remembers: birthdays", "Counter, defaultdict and grouping"),
          ("Structuring data: the chessboard and the picnic", "Modelling a real thing", "Nested dictionaries: the picnic"),
          ("Copies and writing data down", "Copying: alias, shallow and deep", "The notation that carries dictionaries"),
          ("Practice, summary and resources", "Practice: the fantasy game inventory", "Where to go from here")]
_rows = []
for name, a, b in _parts:
    _rows.append("%s (slides %d-%d)" % (name, _t[a], _t[b]))
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 3 or any(_starts[i + 1] != _ends[i] + 1 for i in range(4)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r" % (_starts, _ends))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": str(len(ST.STORIES)), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["notes"] = ("The route has five parts. It starts with the dictionary type and its keys, moves to loops, counting and grouping, "
                 "then to structuring data with a chessboard and a picnic, then to copies and to writing data down, and ends with "
                 "practice, a summary and further resources. The ranges name the exact slides, so you can return to the part "
                 "you need, and four of the slides are true stories that explain where a feature of the language came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 7: Dictionaries and Structuring Data", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
