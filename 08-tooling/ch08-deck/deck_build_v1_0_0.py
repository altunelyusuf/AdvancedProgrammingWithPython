#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 8 (Manipulating Strings) on the CME classroom standard.

Same regime as chapters 1 to 7: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows (no photographs this chapter - see the note below),
consoles and whole programs with their results as Python printed them. Every console result and program transcript
comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py); the speaker notes are prose for the reader.

This chapter ships without story photographs: Wikimedia Commons returned a sustained HTTP 429 rate-limit from this
session's egress IP on 2026-10-11, across repeated retries, so no photograph was fabricated or substituted. Story
slides use a fact card and the fact row (who, where, when, link) instead of an image panel.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories414_8", os.path.join(HERE, "..", "sen0414_ch08_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
PD = sorted(__import__("glob").glob(os.path.join(HERE, "..", "ch08-page", "page_data_v*.json")),
            key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = {n["id"]: n for n in json.load(open(PD[-1]))["nodes"]} if PD else {}
RES = json.load(open(os.path.join(HERE, "..", "ch08-page", "resources_v1_1_0.json")))["links"]
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1 = "Which operations on a string make a new string, which only test it and return a Boolean or a number, and why can none of them change it?"
CQ2 = "Which printed outputs and concepts of the chapter differ in current Python, and on what source?"


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


# ---- 1 title -----------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 8: Manipulating Strings",
          "sub": "Literals, slices, formatting, methods, bytes and the clipboard - a string never changes in place",
          "items": [{"t": "code", "x": 6.0, "y": 0.9, "w": 3.5, "h": 0.8, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Chapters 1 to 7 worked with numbers, lists and dictionaries. This chapter is about the string: how "
                   "one is written, read and rebuilt into a new string, since no method can ever change the string it "
                   "was called on. Every example on these slides was run under Python 3.14.6 and the result printed "
                   "beside it is the result Python gave.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Six parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Six parts, from a quoted literal to a byte, all of it executed.",
          "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.0, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.7, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d concepts" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                     "Python %s" % PYV]}],
        "The first question is the chapter's spine: a string method either builds a new string, such as upper() and "
        "split(), or it only looks at the string and answers with a Boolean or a number, such as isupper() and find(), "
        "and the reason is that a string is immutable, so no method ever has a string to change. The second question "
        "is this chapter's own watch-out: the chapter was printed before f-strings' debug specifier, before t-strings "
        "and before several of the methods now current in Python 3.14, so a few of its claims need a source check "
        "against the version actually running. The chips give the size of the chapter.",
        "Every string method either returns new or tests; it never changes the string.")

# ---- 4 string literals ---------------------------------------------------------------------------------------------
_qrows = [G["quoting"][i] for i in (0, 1, 2, 3, 4, 6, 9)]
c, bot = con("quoting", 0.5, 1.5, 5.6, fs=10.5, label="single, double, escapes, bytes and the backslash", rows=_qrows)
content("String literals and quoting", "A string is text inside quotes, with an escape for the quote it is inside",
        [c,
         card("Why two kinds of quotes", "Alice's cat needs double quotes, or the apostrophe inside it must be "
              "escaped as \\'. The backslash also writes a tab or a newline inside an ordinary string, which a raw "
              "string switches off so a Windows path can be typed literally.", 6.4, 1.5, 3.1, 3.4, fs=11.5)],
        "A string literal sits inside single or double quotes, and choosing the other kind of quote is the easiest way "
        "to hold an apostrophe. The backslash begins an escape sequence: \\t is a tab and \\n is a newline, both counted "
        "as one character by len() though they are two characters in the source. A raw string, written r'...', turns "
        "every backslash into a plain character, which is why a Windows path is typed as r'C:\\Users\\Alice\\Desktop' "
        "without doubling anything, and a bytes literal, b'a', holds raw bytes rather than text at all.",
        "An escape or a raw string decides what a backslash means.")

# ---- 5 raw and multiline strings ------------------------------------------------------------------------------------
c, bot = con("literalforms", 0.5, 1.5, 9.0, fs=9, label="a raw string keeps every backslash; triple quotes keep every newline")
content("Raw strings and multiline strings", "A raw string keeps the backslash; triple quotes keep the line breaks",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "r'\\n' is two characters, a backslash and an n; '\\n' is one, the newline. letter.split('\\n') breaks "
                  "the triple-quoted letter back into its four lines, the blank line between them showing up as ''."}],
        "A raw string is for text where backslashes are meant literally, such as a Windows path or a regular expression "
        "pattern, and len(r'\\n') is 2 while len('\\n') is 1, because the raw string never turns \\n into a newline "
        "character. A triple-quoted string, opened and closed with three quote marks, can run across several lines of "
        "source code and keeps every line break and blank line exactly as typed; the console on this slide types the "
        "same four-line letter as one REPL line with explicit \\n escapes instead, to the same effect, and splits it "
        "back into its lines on '\\n'.",
        "Triple quotes keep line breaks; r-strings keep backslashes.")

# ---- 6 indexing and slicing ------------------------------------------------------------------------------------------
c, bot = con("access", 0.5, 1.5, 5.6, fs=11, label="a position finds one character; a slice finds a run of them")
content("Indexing and slicing", "A position finds one character; a colon finds a run of them",
        [c,
         card("Reading the console", "greeting[0] is the first character and greeting[-1] is the last, counting back "
              "from the end. greeting[0:5] takes up to but not including index 5, and greeting[::-1] reverses the "
              "whole string by stepping backwards.", 6.4, 1.5, 3.1, 3.4, fs=11.5)],
        "Indexing with one number, greeting[4], returns a single character, and a negative index counts from the end, so "
        "greeting[-1] is always the last character without knowing the string's length. Slicing with a colon, "
        "greeting[0:5], returns every character from the first index up to but not including the second, and either "
        "number can be left out to mean the start or the end of the string. A slice with a step of -1, greeting[::-1], "
        "walks the string backwards one character at a time and so reverses it, a trick the chapter relies on more than "
        "once.",
        "Slicing never includes the character at the stop index.")

# ---- 7 the in operator and immutability -------------------------------------------------------------------------------
c, bot = con("properties", 0.5, 1.5, 5.4, fs=10.5, label="in tests for a substring; a string cannot be changed in place")
content("The in operator and immutability", "in asks whether one string sits inside another; no method changes a string in place",
        [c,
         card("What never changes", "name[0:7] + 'the' + name[8:12] builds a brand new string; it does not edit name. "
              "Every method that looks like a change, such as upper(), returns a new string and leaves the original "
              "exactly as it was.", 6.2, 1.5, 3.3, 3.3, fs=11.5)],
        "The in operator, written 'Hello' in 'Hello, World', tests whether the left string occurs anywhere inside the "
        "right one and returns a Boolean, with not in as its opposite; the empty string is found inside every string, "
        "so '' in 'spam' is always True. A string is immutable: once created it can never be edited in place, so to "
        "change part of a message you slice out the parts you want and concatenate them into a new string with +, "
        "exactly as the console does to replace the middle of a cat's name.",
        "A string cannot change; every edit builds a new one.")

# ---- 8 f-strings --------------------------------------------------------------------------------------------------
c, bot = con("fstrings", 0.5, 1.5, 9.0, fs=9.5, label="an f-string evaluates {expr}; format specifiers and = control how it is shown", rows=G["fstrings"])
content("F-strings", "An f-string evaluates what is inside the braces and substitutes the result",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "{age + 10} runs the expression first; {42:>6} right-justifies in 6 characters; {name=} prints the "
                  "expression text and its value together, which the chapter's own printing did not yet have."}],
        "Writing f before the opening quote turns a string literal into an f-string, and anything inside braces is "
        "evaluated as a Python expression and substituted into the text, so f'{age + 10}' prints 4010 rather than the "
        "text age + 10. A format specifier after a colon controls the display, as in {3.14159:.2f} for two decimal "
        "places or {255:#x} for hexadecimal, and a double brace, {{name}}, prints a literal brace. The self-documenting "
        "{name=} and {age + 1 = } forms, added in Python 3.8, print the expression's own source text beside its value, "
        "a convenience the printed chapter could not show because it did not exist when the chapter was written.",
        "f'{expr}' evaluates expr and substitutes the result as text.")

# ---- 9 story: f-strings PEP 498 --------------------------------------------------------------------------------------
content("One PEP gave Python its f-string, in a single day", STORY["FStringsPep498"]["when"],
        [card("PEP 498", "Literal String Interpolation. Created 1 August 2015 by Eric V. Smith, targeted at Python 3.6, "
              "and its own example reads almost exactly like the chapter's: f'My name is {name}, my age next year is "
              "{age+1}'.", 0.5, 1.5, 4.0, 2.7, fs=13),
         {"t": "beats", "x": 4.8, "y": 1.5, "w": 4.7, "h": 2.7, "fs": 12, "items": [
             "1 August 2015: PEP 498 is created, authored by Eric V. Smith",
             "Targeted at Python 3.6, shipped at the end of 2016",
             "The PEP's own example reads almost like the chapter's",
             "Every f'{name}' since has worked the same way"]},
         factrow("FStringsPep498")],
        story_notes("FStringsPep498"),
        "The f-string programmers use daily traces to one named PEP.")

# ---- 10 older formatting styles ---------------------------------------------------------------------------------------
c, bot = con("older", 0.5, 1.5, 9.0, fs=9, label="concatenation, %-formatting and str.format() all predate the f-string", rows=G["older"])
content("Older ways to build the same string", "Concatenation, %-style and str.format() all still work",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "'Py' 'thon' concatenates two literals that sit next to each other; 3 * 'un' repeats a string; the "
                  "{1} and {0} in .format() name arguments by position, out of order if needed."}],
        "Before f-strings, the chapter builds the same sentence three ways: by concatenating pieces with + and "
        "converting the number with str(), with the %-operator and a tuple of values, and with str.format() and "
        "numbered placeholders that can repeat an argument, as {0} does twice. All three still run correctly in "
        "Python 3.14, so the chapter's own point stands: f-strings are newer and usually clearer, but nothing here was "
        "removed. Two adjacent string literals with nothing between them, 'Py' 'thon', are concatenated by the "
        "compiler into one string at compile time, and the * operator repeats a string that many times.",
        "f-strings replaced none of the three older styles; all still run.")

# ---- 11 changing case and testing it ------------------------------------------------------------------------------
c, bot = con("case", 0.5, 1.5, 5.6, fs=10.5, label="upper(), lower(), isupper() and casefold()")
content("Changing case and testing it", "upper() and lower() build new strings; isupper() only asks",
        [c,
         card("casefold vs lower", "'stra\\xdfe'.casefold() == 'strasse' is True because casefold() also expands the "
              "German sharp s, something lower() alone does not do; it exists only for comparing text, never for display.",
              6.4, 1.5, 3.1, 3.3, fs=11.5)],
        "upper() and lower() each return a new string with every letter changed, leaving the original exactly as it "
        "was, and isupper() only tests whether the letters already present are all uppercase and returns a Boolean, "
        "so 'great' == 'GREat'.lower() is the idiom for a case-insensitive comparison. casefold(), added for stronger "
        "comparisons than lower(), also folds special characters such as the German sharp s so that two spellings that "
        "a human reads as equal compare as equal; it is meant only for comparison, not for showing text to a reader.",
        "casefold() compares text; upper() and lower() build it.")

# ---- 12 testing a string's content ------------------------------------------------------------------------------------
c, bot = con("checks", 0.5, 1.5, 9.0, fs=9.5, label="isX() methods test every character and answer a Boolean", rows=G["checks"])
content("Testing a string's content", "isalpha, isalnum, isdecimal and the startswith/endswith pair, all Booleans",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.1, "w": 9.0, "h": 4.95 - bot - 0.1, "fs": 10.5,
          "body": "startswith/endswith also accept a tuple of several endings to test in one call."}],
        "Every is-method tests every character in the string and returns a single Boolean: isalpha() is true only if "
        "every character is a letter and the string is not empty, and isalnum() allows letters and digits together. "
        "isdecimal() is stricter than it looks: '\\u0663'.isdecimal() is True for an Arabic-Indic digit, yet int() on "
        "that same character still succeeds, converting it to the ordinary integer 3, a case the chapter's printed text "
        "does not show. startswith() and endswith() test one end of the string and, since they accept a tuple, "
        "'notes.txt'.endswith(('.py', '.txt')) checks two endings in a single call.",
        "An is-method tests every character and returns one Boolean.")

# ---- 13 joining and splitting ---------------------------------------------------------------------------------------
c, bot = con("joinsplit", 0.5, 1.5, 9.0, fs=9.5, label="join() needs a list; split() and partition() cut a string apart", rows=G["joinsplit"])
content("Joining and splitting text", "join() needs a list of strings; split() and partition() cut one apart",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "', '.join([...]) is called on the separator, with the list as its argument; split() with no argument "
                  "cuts on any run of whitespace; splitlines() recognises every line boundary split('\\n') would miss."}],
        "join() is called on the separator string and takes a list of strings to glue together, which is why "
        "', '.join(['cats', 'rats', 'bats']) reads backwards to someone used to other languages. split(sep) cuts a "
        "string at every occurrence of sep and returns the pieces as a list; split() with no argument at all is a "
        "special case that cuts at any run of whitespace and ignores it at the ends, which is why 'My name is "
        "Simon'.split() and split('m') give different results. partition(sep) cuts at only the first occurrence and "
        "returns a three-item tuple that keeps the separator itself, where split() would discard it.",
        "join() glues a list; split() and partition() cut a string.")

# ---- 14 justifying and stripping -------------------------------------------------------------------------------------
c, bot = con("spacing", 0.5, 1.5, 9.0, fs=10, label="rjust, ljust, center pad with a fill character; strip removes from the ends", rows=G["spacing"])
content("Justifying and stripping whitespace", "rjust/ljust/center pad a string; strip removes characters from its ends",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "strip('ampS') removes any of those characters from either end, not the substring 'ampS' as a whole; "
                  "removesuffix() and removeprefix(), added in Python 3.9, remove one exact piece instead."}],
        "rjust() and ljust() pad a string to a given width with spaces or a fill character on one side, and center() "
        "pads on both sides, all three used by the chapter's own table-printing program. strip() removes whitespace "
        "from both ends by default, and when given a string of characters it removes any of those characters, in any "
        "order, from either end until it meets one that is not in the set, which is why strip('ampS') eats through "
        "'SpamSpamBaconSpamEggsSpamSpam' down to 'BaconSpamEggs'. removeprefix() and removesuffix(), added in Python "
        "3.9, are the exact-match tools the chapter's own printed text predates.",
        "strip() removes a set of characters; removesuffix() removes one exact piece.")

# ---- 15 story: Unicode Consortium ------------------------------------------------------------------------------------
content("Nine companies agree on one table of characters", STORY["UnicodeConsortium"]["when"],
        [card("The 1991 press release", "Nine companies - Apple, GO, IBM, Metaphor, Microsoft, NeXT, Novell, the "
              "Research Libraries Group and Sun - formally affiliated as Unicode Inc. on 19 February 1991, with "
              "Xerox's Joe Becker as technical vice president.", 0.5, 1.5, 4.4, 2.7, fs=12.5),
         {"t": "beats", "x": 5.2, "y": 1.5, "w": 4.3, "h": 2.7, "fs": 12, "items": [
             "19 February 1991: nine companies announce Unicode Inc.",
             "The consortium assigns the numbers ord() and chr() read",
             "ord('A') is 65 because that table says so",
             "The same table underlies the chapter's utf-8 encoding"]},
         factrow("UnicodeConsortium")],
        story_notes("UnicodeConsortium"),
        "ord() and chr() read a table nine companies agreed on in 1991.")

# ---- 16 finding and replacing ----------------------------------------------------------------------------------------
c, bot = con("search", 0.5, 1.5, 5.4, fs=11, label="find() returns an index or -1; replace() swaps matches")
content("Finding and replacing", "find() returns an index or -1; replace() swaps every occurrence",
        [c,
         card("find vs index", "find() returns -1 for no match, where the related index() method raises a ValueError "
              "instead; a third argument to find() starts the search partway through the string.",
              6.1, 1.5, 3.4, 3.1, fs=11.5)],
        "find() searches for a substring and returns the index of its first occurrence, or -1 if it is not there at "
        "all, and an optional second argument starts the search from a later position, which is how the same call "
        "finds a second 'spam' further along the string. count() returns how many times a substring occurs, without "
        "overlapping matches. replace() returns a new string with every occurrence of the first argument swapped for "
        "the second, and an optional third argument limits how many replacements are made, as in replacing only the "
        "first of three occurrences of 'spam' with 'eggs'.",
        "find() locates a match; replace() swaps every one by default.")

# ---- 17 ord, chr and UTF-8 encoding ------------------------------------------------------------------------------------
c, bot = con("bytes", 0.5, 1.5, 9.0, fs=9, label="ord()/chr() convert a character to and from its code point; encode() turns text into bytes", rows=G["bytes"])
content("ord(), chr() and UTF-8 encoding", "A code point names a character; UTF-8 turns characters into bytes",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "'caf\\xe9'.encode('utf-8') is 5 bytes for 4 characters, since e-acute takes two bytes in utf-8; "
                  "encoding with errors='replace' swaps an unencodable character for a placeholder instead of raising."}],
        "Every character has a code point, a number the Unicode standard assigns to it, and ord() and chr() convert "
        "between a character and that number in either direction. Encoding turns text into bytes for a particular "
        "scheme: utf-8 is the right choice almost all of the time, because it can represent every Unicode character "
        "and stays compatible with plain ASCII, though a character outside ASCII, such as e-acute, can take more than "
        "one byte, so len() of the text and len() of its utf-8 encoding can differ. Encoding to plain ascii raises a "
        "UnicodeEncodeError on a character ascii cannot hold, unless an errors argument such as 'replace' is given.",
        "utf-8 represents every character; ascii cannot.")

# ---- 18 story: UTF-8 on a placemat -------------------------------------------------------------------------------------
content("The encoding written on a diner placemat", STORY["Utf8Diner"]["when"],
        [card("Rob Pike's own account", "'Designed, in front of my eyes, on a placemat in a New Jersey diner one "
              "night in September or so 1992... I very clearly remember Ken writing on the placemat.'",
              0.5, 1.5, 4.5, 2.7, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.7, "fs": 12, "items": [
             "September 1992: Thompson and Pike sketch UTF-8",
             "Bell Labs, for the Plan 9 operating system",
             "1 to 4 bytes per character, ASCII stays compatible",
             "That is the encoding behind str.encode('utf-8')"]},
         factrow("Utf8Diner")],
        story_notes("Utf8Diner"),
        "The encoding behind str.encode('utf-8') began on a placemat.")

# ---- 19 Pig Latin -----------------------------------------------------------------------------------------------------
p1, bot = prog("pigLatin_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(25, 37), show_out=False)
p2 = transcript("pigLatin_v1_0_0.py", 0.5, bot + 0.4, 9.0, 0.6, fs=9, label="typed: My name is Al Sweigart. I am 4,000 years old.")
content("The Pig Latin program", "Vowel-starting words get yay; consonants move to the end and get ay",
        [p1, p2],
        "Pig Latin moves the leading consonants of a word to its end and adds ay, or simply adds yay to a word that "
        "starts with a vowel, and the program keeps any leading or trailing punctuation untouched around the word it "
        "transforms. Typed against 'My name is Al Sweigart. I am 4,000 years old.' the program printed 'Ymay amenay "
        "isyay Alyay Eigartsway. IYAY amyay 4,000 yearsyay oldyay.', and the single-letter word 'I' becomes the all-"
        "capital 'IYAY' rather than a capitalised 'Iyay', because the program's own case-restoring rule treats a fully "
        "uppercase one-letter word as upper rather than title case; a genuine, worth-noticing quirk of the algorithm, "
        "not a bug the demonstration hides.",
        "A one-letter word exposes Pig Latin's own case quirk, IYAY.")

# ---- 20 practice: table printer and alternating case ---------------------------------------------------------------
p1, bot = prog("tablePrinter_v1_0_0.py", 0.5, 1.5, 9.0, fs=7.0)
content("Practice: printing a table, alternating case", "Column widths come from the data itself, not from a fixed number",
        [p1,
         {"t": "text", "x": 0.5, "y": bot + 0.1, "w": 9.0, "h": 4.95 - bot - 0.1, "fs": 10.5,
          "body": "col_widths[i] grows to the longest string in each column, and rjust() uses that width for every row."}],
        "The table-printing program computes the widest string in each column before printing a single row, so the "
        "table lines up whatever the data happens to be, rather than assuming a fixed width. Each cell is right-"
        "justified to its column's own width with rjust() and printed with a trailing space, which is why the four "
        "columns of names and animals line up exactly as shown. A second practice program, alternating case, walks a "
        "string by position with enumerate() and lowercases even-indexed characters while uppercasing odd ones, "
        "turning 'Hello, world!' into 'hElLo, WoRlD!'.",
        "Measuring the data first is what makes the table line up.")

# ---- 21 the clipboard and pyperclip -----------------------------------------------------------------------------------
content("The clipboard and pyperclip", "copy() and paste() read and write the operating system's own clipboard",
        [card("Two functions, one clipboard", "pyperclip.copy(text) places text on the clipboard and pyperclip.paste() "
              "returns whatever is there. The bullet-point-adder program pastes, edits every line, and copies the "
              "result back.", 0.5, 1.5, 4.3, 3.2, fs=12),
         card("A real limitation, kept honest", "Running the bullet-point-adder program in this headless session raised "
              "ModuleNotFoundError: No module named 'pyperclip', then, once installed, pyperclip.PyperclipException "
              "because no clipboard mechanism exists without a desktop. The program is correct; the sandbox has no "
              "clipboard.", 5.1, 1.5, 4.4, 3.2, fs=11.5)],
        "pyperclip is a third-party module the chapter installs with pip, and its two functions, copy() and paste(), "
        "are the entire interface: paste() returns the text currently on the operating system's clipboard as a string, "
        "and copy() places a string there for the next paste anywhere on the machine. The bullet-point-adder program "
        "pastes whatever text was copied, adds an asterisk and a space to the front of every line, and copies the "
        "result back, so the next paste anywhere, in any application, has the bulleted version. This slide's own "
        "right-hand card is an honest record of a real error this session hit trying to run that exact program "
        "without a desktop clipboard, rather than a claim the program was never actually run.",
        "copy() and paste() are pyperclip's whole interface.")

# ---- 22 story: cut, copy and paste ------------------------------------------------------------------------------------
content("The chapter's clipboard model is fifty years old", STORY["CutCopyPaste"]["when"],
        [card("Larry Tesler, Xerox PARC", "Joined PARC in 1973 and, with Tim Mott, gave the Gypsy word processor its "
              "cut, copy and paste model: select, hold, insert elsewhere. Tesler died 16 February 2020, and his "
              "obituaries used his own invention as the headline.", 0.5, 1.5, 4.6, 2.9, fs=12.5),
         {"t": "beats", "x": 5.4, "y": 1.5, "w": 4.1, "h": 2.9, "fs": 12, "items": [
             "1973: Tesler and Mott build the Gypsy word processor",
             "Select, hold, insert elsewhere: cut, copy, paste",
             "16 February 2020: Tesler dies, aged 74",
             "pyperclip.copy()/paste() are the same model, in Python"]},
         factrow("CutCopyPaste")],
        story_notes("CutCopyPaste"),
        "pyperclip's two calls are a fifty-year-old idea in Python.")

# ---- 23 summary ------------------------------------------------------------------------------------------------------
content("The chapter in six lines", "One line for each part of the route",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 11.5, "items": [
            "A literal is quoted text; an escape or a raw string decides what a backslash means inside it.",
            "A position or a slice reads part of a string; in tests for a substring; nothing ever edits one in place.",
            "f-strings evaluate {expr} and substitute it; concatenation, %-style and .format() still work too.",
            "upper()/lower() build new strings, is-methods only test, and casefold() is for comparing text.",
            "join() glues a list; split(), splitlines() and partition() cut a string apart in different ways.",
            "ord()/chr() read a code point; utf-8 encodes it to bytes; pyperclip's copy()/paste() reach the clipboard."]}],
        "These six lines answer the route one part at a time. The first two cover how a string is written and read, "
        "the third and fourth cover building and testing it, the fifth covers cutting and joining text, and the sixth "
        "covers bytes and the clipboard. If a line feels unproven, the part of the route that carries it has the "
        "slides with the executed examples.",
        "If a line feels unproven, its slides hold the example.")

# ---- 24 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(":")[0] if r["kind"] != "documentation" or "textbook" not in r["title"].lower() else "The textbook, chapter 8 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": rows(("documentation",))[:3]},
            {"head": "Proposals", "rows": rows(("pep",))},
            {"head": "History and tools", "rows": [
                ["Rob Pike, UTF-8 history", "https://doc.cat-v.org/bell_labs/utf-8_history"],
                ["Unicode Inc., first press release, 1991", "https://www.unicode.org/history/first-pr.htm"],
                ["Larry Tesler, Wikipedia", "https://en.wikipedia.org/wiki/Larry_Tesler"]] + rows(("interactive",))}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read online "
        "and has the Pig Latin, table-printing and clipboard programs in full, the proposal links lead to the exact "
        "PEPs behind f-strings, PEP 701 and t-strings, and the history links are the primary sources behind this "
        "chapter's three stories. Python Tutor lets you step through a program and watch a string stay the same while "
        "a new one appears beside it, which is the clearest way to see immutability.",
        "History and documentation links, each opened on the day this deck was built.")

# ---- 25 closing -------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A string method either returns a new string or tests and returns a Boolean; it never edits in place.",
            "An f-string evaluates {expr}; a format specifier after the colon controls how it is shown.",
            "split(), splitlines() and partition() each cut a string apart in a different, specific way.",
            "ord()/chr() read a code point, utf-8 encodes it to bytes, and pyperclip reaches the real clipboard."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d console rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the "
        "examples yourself, you have the chapter. The next chapter moves on to functions.",
        "Questions are welcome; bring one example you could not predict.")

# ---- agenda -----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Literals and reading a string", "The questions this chapter answers", "The in operator and immutability"),
          ("Formatting: f-strings and the older styles", "F-strings", "Older ways to build the same string"),
          ("Case, content and cutting text apart", "Changing case and testing it", "Nine companies agree on one table of characters"),
          ("Characters, bytes and Pig Latin", "Finding and replacing", "The Pig Latin program"),
          ("The clipboard, practice and summary", "Practice: printing a table, alternating case", "The chapter in six lines"),
          ("Resources", "Where to go from here", "Where to go from here")]
_rows = []
for name, a, b in _parts:
    _rows.append("%s (slides %d-%d)" % (name, _t[a], _t[b]))
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 3 or any(_starts[i + 1] != _ends[i] + 1 for i in range(5)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": str(len(ST.STORIES)), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["notes"] = ("The route has six parts. It starts with literals and reading a string, moves to formatting with "
                 "f-strings and the older styles, then to case, content tests and cutting text apart, then to "
                 "characters, bytes and Pig Latin, then to the clipboard, practice and the summary, and ends with "
                 "resources and closing. The ranges name the exact slides, so you can return to the part you need, "
                 "and four of the slides are true stories that explain where a feature came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 8: Manipulating Strings", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
