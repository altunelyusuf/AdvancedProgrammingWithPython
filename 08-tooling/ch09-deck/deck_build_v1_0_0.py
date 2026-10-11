#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 9 (Text Pattern Matching with Regular Expressions) on the CME
classroom standard.

Same regime as the earlier chapters: numbered warm-ivory slides, an agenda with exact slide ranges, a summary
before the resources, full-sentence takeaway strips, stories with fact rows (no photographs this chapter - see the
note below), consoles and whole programs with their results as Python printed them. Every console result and
program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py); the speaker notes are
prose for the reader.

This chapter ships without story photographs: Wikimedia Commons returned a sustained HTTP 429 rate-limit from this
session's egress IP on 2026-10-11, across repeated retries, the same condition chapter 8 recorded, so no
photograph was fabricated or substituted. Story slides use a fact card and the fact row (who, where, when, link)
instead of an image panel.

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


ST = load("stories414_9", os.path.join(HERE, "..", "sen0414_ch09_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
PD = sorted(__import__("glob").glob(os.path.join(HERE, "..", "ch09-page", "page_data_v*.json")),
            key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = {n["id"]: n for n in json.load(open(PD[-1]))["nodes"]} if PD else {}
RES = json.load(open(os.path.join(HERE, "..", "ch09-page", "resources_v1_0_0.json")))["links"]
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1 = ("Which part of a pattern decides what one position matches, how many times it repeats, where it must sit, "
       "and which pair of parentheses keeps the text once a match is found?")
CQ2 = "Which printed outputs and quirks of the chapter differ in current Python, and on what source?"


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


# ---- 1 title ---------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 9: Regular Expressions",
          "sub": "Writing a pattern once, compiling it, and asking it to search, find, or replace",
          "items": [{"t": "code", "x": 6.0, "y": 0.85, "w": 3.5, "h": 0.95, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Chapter 8 was about a string once you already had it. This chapter is about finding one: a "
                   "regular expression is a small language, written inside a string, for describing the shape of "
                   "text rather than its exact characters, and the re module compiles that description once and "
                   "then asks it to search, find every match, or replace what it finds. Every example on these "
                   "slides was run under Python 3.14.6 and the result printed beside it is the result Python gave.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Six parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Six parts, from a hand-written check to a human-readable module.",
          "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["4 branches", "%d concepts" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                     "Python %s" % PYV]}],
        "The first question is the chapter's own spine: a pattern's syntax answers four separate questions - what "
        "may sit at one position (a character set or a shorthand class), how many times it repeats (a quantifier, "
        "greedy or lazy), where it must sit (an anchor), and what the match keeps for later (a group) - and a "
        "method such as search, findall or sub then does something with the answer. The second question is this "
        "chapter's own watch-out: the chapter was printed before Python renamed its own error type, before its own "
        "dollar sign and word-boundary behaviour were clarified in the documentation, and before Humre reached a "
        "release that differs from the chapter's own listing, so a few of its claims need a source check against "
        "the version actually running. The chips give the size of the chapter.",
        "A pattern answers what, how many, where, and what is kept.")

# ---- 4 manual matching, no regex yet --------------------------------------------------------------------------------
c, bot = con("manual", 0.5, 1.5, 9.0, fs=9.5, label="is_phone_number() tests length, digits and hyphen positions by hand")
content("Finding patterns without a regular expression", "A phone number can be tested position by position, with no pattern language at all",
        [c,
         card("Reading is_phone_number", "The function tests that the text is exactly 12 characters long, that "
              "positions 0 to 2, 4 to 6 and 8 to 11 are each digits, and that positions 3 and 7 are each a hyphen - "
              "the same shape a regular expression will soon describe in one line instead of five.",
              0.5, bot + 0.12, 9.0, 4.95 - bot - 0.12, fs=11.5)],
        "Before the re module appears, the chapter writes is_phone_number() by hand: it rejects any text that is "
        "not exactly twelve characters, then checks that the three digit groups are each decimal with isdecimal() "
        "and that a hyphen sits at positions 3 and 7, exactly where a phone number such as 415-555-1011 needs one. "
        "A list comprehension slides a twelve-character window across a longer message and keeps only the slices "
        "that pass the test, which is how the message in this console yields its two phone numbers and ignores "
        "everything else; 'Moshi moshi' fails immediately because it is not even the right length.",
        "A hand-written check like this is exactly what a pattern will replace.")

# ---- 5 pattern objects: compile then search -------------------------------------------------------------------------
c, bot = con("objects", 0.5, 1.5, 9.0, fs=8, label="compile() builds a Pattern object; search() returns a Match or None")
content("Pattern objects: compile, then search", "re.compile() builds a Pattern once; its search() returns a Match object or None",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "mo.group() returns the whole matched text and mo.span() returns the (start, end) indices; a "
                  "search that fails returns None rather than raising, so testing a Match object's truth is safe. "
                  "match() anchors only at the start of the string and fullmatch() requires the whole string."}],
        "re.compile() turns a pattern string into a Pattern object, and compiling once before searching many times "
        "is both the documented idiom and the chapter's own practice. The Pattern's search() method scans the text "
        "for the first place the pattern matches and returns a Match object holding that result, or None if the "
        "pattern is not found anywhere, which is why phoneNumRegex.search('no digits here') prints nothing rather "
        "than raising an error. match() and fullmatch(), both shown here, are the stricter relatives search() has: "
        "match() only tries the very start of the string, and fullmatch() additionally requires the match to reach "
        "the string's end.",
        "search() returns a Match or None; it never raises on no match.")

# ---- 6 story: Thompson 1968 ------------------------------------------------------------------------------------------
content("A 1968 paper is why compile() comes before search()", STORY["ThompsonRegexSearch"]["when"],
        [card("Ken Thompson, CACM 1968", "'Regular Expression Search Algorithm', Communications of the ACM, "
              "volume 11, number 6, June 1968: compile a pattern once into a form that simulates an automaton, "
              "then search text against that compiled form.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "June 1968: CACM 11(6), article 12736, Ken Thompson",
             "Built first into the QED editor at Bell Labs",
             "US Patent 3,568,156 for the technique",
             "re.compile() then search() is the same two steps"]},
         factrow("ThompsonRegexSearch")],
        story_notes("ThompsonRegexSearch"),
        "re.compile() then search() is Ken Thompson's 1968 two-step algorithm.")

# ---- 7 story: Secret Labs' engine, 1999 -------------------------------------------------------------------------------
content("A company's own engine, still runs under re", STORY["SreBecomesRe"]["when"],
        [card("Secret Labs AB, _sre.c", "Python's C source behind every Match object carries a change log opening "
              "24 October 1999, crediting 'fl' and Secret Labs AB, reachable at info@pythonware.com, with Hewlett-"
              "Packard funding its move into Python 1.6.", 0.5, 1.5, 4.6, 2.9, fs=12.5),
         {"t": "beats", "x": 5.4, "y": 1.5, "w": 4.1, "h": 2.9, "fs": 12, "items": [
             "24 Oct 1999: the _sre.c history log begins",
             "Secret Labs AB holds copyright, 1997 to 2001",
             "Martin von Loewis adds wide character support",
             "mo.group() and mo.span() reach that same engine"]},
         factrow("SreBecomesRe")],
        story_notes("SreBecomesRe"),
        "mo.group() and mo.span() reach a C engine logged since 1999.")

# ---- 8 grouping ------------------------------------------------------------------------------------------------------
c, bot = con("grouping", 0.5, 1.5, 9.0, fs=8, label="parentheses number a group from 1; the pipe tries alternatives; (?P<name>...) names one")
content("Grouping: parentheses, the pipe, and names", "Parentheses number a group; the pipe offers alternatives; (?P<name>...) names a group",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "groups() returns every group's text as a tuple in order; groupdict() does the same by name for "
                  "a pattern written with (?P<name>...); \\1 inside a pattern repeats whatever group 1 matched."}],
        "Parentheses around part of a pattern create a group, numbered from 1 in the order the opening parentheses "
        "appear, and group(1), group(2) and groups() read the text each one matched out of a Match object. The "
        "pipe inside parentheses offers several alternatives and tries them left to right, taking the first one "
        "that matches, which is why Cat(erpillar|astrophe|ch|egory) matches 'Catch' by trying erpillar and "
        "astrophe first and finding neither. A named group, written (?P<name>...), is read by groupdict() as well "
        "as by number, and a back reference inside the pattern itself, \\1, requires group 1's own match to repeat "
        "verbatim, which is how 'this is is a typo' is caught as a doubled word.",
        "Parentheses group and number; the pipe offers alternatives.")

# ---- 9 story: Kleene 1951 ---------------------------------------------------------------------------------------------
content("A mathematician named the pattern, in 1951", STORY["KleeneRegularEvents"]["when"],
        [card("Stephen Cole Kleene, RAND 1951", "Research Memorandum RM-704 defined a regular event from three "
              "operations: concatenation, union and repetition. Kleene worked at the University of Wisconsin-"
              "Madison from 1935 to 1979.", 0.5, 1.5, 4.4, 2.8, fs=12.5),
         {"t": "beats", "x": 5.2, "y": 1.5, "w": 4.3, "h": 2.8, "fs": 12, "items": [
             "1951: RM-704, RAND Corporation, Santa Monica",
             "Union = the pipe this chapter calls alternation",
             "Repetition = the star and plus quantifiers",
             "Kleene: born 5 Jan 1909, died 25 Jan 1994"]},
         factrow("KleeneRegularEvents")],
        story_notes("KleeneRegularEvents"),
        "The pipe and the star are Kleene's 1951 union and repetition.")

# ---- 10 character sets -------------------------------------------------------------------------------------------
c, bot = con("charsets", 0.5, 1.5, 5.6, fs=11, label="a class matches one character; a shorthand stands for one")
content("Character sets and shorthand classes", "Square brackets name a set of characters; \\d, \\w and \\s stand for whole sets",
        [c,
         card("Negation and the dot", "A caret right after the opening bracket negates the class, so "
              "[^aeiouAEIOU] matches any character that is not a vowel; the dot matches almost any single "
              "character at all, vowel, consonant, digit or space alike.", 6.4, 1.5, 3.1, 3.3, fs=11.5)],
        "A character class in square brackets, [aeiouAEIOU], matches exactly one character from the set listed "
        "inside it, and a caret right after the opening bracket negates the class instead, matching any character "
        "not in the set. The shorthand classes \\d, \\w and \\s stand for a digit, a word character and whitespace "
        "respectively, with their capitalised opposites \\D, \\W and \\S, and the chapter's own documentation now "
        "notes that \\d matches any Unicode decimal digit, not only 0 to 9, unless the pattern is compiled with "
        "re.ASCII. \\d+\\s\\w+ finds a run of digits, one space, and a run of word characters together, which is "
        "how '12 drummers' is pulled whole out of a longer list.",
        "Brackets name a set; \\d, \\w and \\s are whole sets by name.")

# ---- 11 story: Perl 1987 -----------------------------------------------------------------------------------------
content("\\d, \\w and \\s came from a language, in 1987", STORY["PerlShorthandClasses"]["when"],
        [card("Larry Wall, Perl 1.0", "Released 18 December 1987 at Unisys; Perl 2 (June 1988) shipped the "
              "backslash shorthand classes this chapter still uses. Python's own re documentation opens by citing "
              "Perl.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "18 Dec 1987: Perl 1.0, Larry Wall, Unisys",
             "June 1988: Perl 2's stronger regex engine",
             "\\d \\w \\s travel with Perl's own popularity",
             "Python's re docs: 'similar to those in Perl'"]},
         factrow("PerlShorthandClasses")],
        story_notes("PerlShorthandClasses"),
        "\\d, \\w and \\s travelled into Python from Perl, released in 1987.")

# ---- 12 repetition ----------------------------------------------------------------------------------------------
c, bot = con("repetition", 0.5, 1.5, 9.0, fs=7.5, label="?, *, + and {m,n} choose how many; a trailing ? on any of them makes it lazy")
content("Repetition: quantifiers, greedy and lazy", "A question mark, star, plus or brace says how many; a trailing ? takes as few as it can",
        [c],
        "A question mark makes the item before it optional, zero or one time; a star matches it zero or more "
        "times; a plus requires at least one; and curly brackets give an exact count, {3,5}, or an open range. "
        "Every one of these quantifiers is greedy by default, taking as many repetitions as it can and backing off "
        "only if the rest of the pattern then fails, which is why (Ha){3,5} against five Ha's takes all five; a "
        "trailing question mark after any quantifier makes it lazy instead, taking as few repetitions as it can, "
        "which is why <.*?> stops at the first '>' it finds instead of the last. The same greedy-versus-lazy choice "
        "is why .* and .*? give very different answers against text with more than one closing character. A word "
        "of caution worth repeating from the chapter itself: its own printed Eggs( and spam)* example has a "
        "leading space inside the group, where this console's pattern has none, so the span printed here, (0, "
        "22), is correct for this console's own pattern and should not be read as a claim about the chapter's.",
        "Every quantifier is greedy by default; a trailing ? makes it lazy.")

# ---- 13 anchors --------------------------------------------------------------------------------------------------
c, bot = con("anchors", 0.5, 1.5, 9.0, fs=10, label="^ and $ anchor to the string's ends; \\b/\\B test a word's edge; look-around tests without consuming")
content("Anchors: start, end, word boundary, look-around", "^ and $ anchor the string; \\b/\\B test a word's edge; look-around tests without consuming",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 9.5,
          "body": "The documentation, not the chapter's wording, is the one to trust on $: it matches at the "
                  "very end of the string or just before a trailing newline, so ^\\d+$ also matches '123\\n'."}],
        "A caret at the start of a pattern anchors it to the start of the string and a dollar sign anchors it to "
        "the end, so re.fullmatch is not the only way to require the whole string to match. \\b marks the boundary "
        "between a word character and a non-word character, and its opposite \\B marks a position that is not "
        "such a boundary, which is how \\Bcat\\B finds 'cat' buried inside 'certificate' but not a 'cat' standing "
        "at a word's edge. A lookahead, (?= dollars), and a lookbehind, (?<=\\$), each test the text beside a "
        "position without consuming it, so \\d+(?= dollars) returns the digits alone, with the word 'dollars' left "
        "in the text for whatever is searched next.",
        "A look-around tests text beside a position without consuming it.")

# ---- 14 finding every match ----------------------------------------------------------------------------------------
c, bot = con("finding", 0.5, 1.5, 9.0, fs=8.5, label="findall returns strings or tuples, never overlapping; finditer gives each Match in turn")
content("Finding every match: findall and finditer", "findall returns every non-overlapping match; finditer hands back each Match object in turn",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11.5,
          "body": "findall returns a plain list of strings when the pattern has no groups or exactly one, and a "
                  "list of tuples of group text when it has two or more; finditer gives up nothing but the Match "
                  "objects themselves, each with its own start(), end() and group()."}],
        "findall() searches the whole text and returns every match it finds without overlapping, in order; the "
        "shape of what comes back depends entirely on the pattern's own groups, a plain list of matched strings "
        "for no groups or exactly one, and a list of tuples of each group's text once there are two or more, which "
        "is why (\\w+)=(\\d+) returns a list of (name, number) pairs rather than a list of the whole matched text. "
        "finditer() is the same search but returns an iterator of Match objects instead of committing to one shape "
        "up front, which is how this console reads off each match's own start() and end() position alongside its "
        "text.",
        "A pattern's own groups decide findall's shape: strings or tuples.")

# ---- 15 replacing text with sub() ------------------------------------------------------------------------------------
c, bot = con("replacing", 0.5, 1.5, 9.0, fs=9.5, label="sub(repl, text) replaces every match; repl may be a string with \\1 or a function")
content("Replacing text with sub()", "sub(repl, string) replaces every match; the replacement can name a group, or be a function",
        [c,
         {"t": "text", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 4.95 - bot - 0.12, "fs": 11,
          "body": "The documentation's own signature is sub(repl, string, count=0), the replacement first, the "
                  "text second, matching the order shown here rather than the order the chapter describes it in; "
                  "passing count positionally is deprecated since Python 3.13."}],
        "sub(), called on a compiled Pattern, returns a new string with every match of the pattern replaced by the "
        "given replacement, leaving the original string untouched exactly as every other string operation does. "
        "The replacement can hold a back reference, \\1, to keep part of what matched while replacing the rest, as "
        "'Agent (\\w)\\w*' keeps the first letter of each agent's name and replaces the rest with asterisks. The "
        "replacement can also be a function instead of a string: re.sub() calls it once per match with the Match "
        "object and substitutes whatever it returns, which is how every number in '3 cats 12 dogs' is doubled in "
        "one call. escape() returns a pattern that matches a literal string exactly, backslash-escaping every "
        "character a pattern would otherwise treat specially.",
        "The replacement can hold \\1, or be a function run per match.")

# ---- 16 flags ------------------------------------------------------------------------------------------------------
c, bot = con("flags", 0.5, 1.5, 9.0, fs=9, label="re.I ignores case; re.S lets the dot match a newline; re.X allows comments", rows=G["flags"])
content("Flags: ignorecase, dotall, verbose, and combined", "re.I, re.S, re.X change how a pattern reads; the pipe combines any of them into one flag",
        [c,
         card("A verbose-mode gotcha", "A # comment in VERBOSE mode runs to the pattern's own line break; the "
              "console's \\n after '# area code' is two characters, not a real newline, so the comment swallows "
              "the rest of the pattern and only \\d{3} is left to match.", 0.5, bot + 0.1, 9.0, 4.95 - bot - 0.1, fs=10)],
        "re.IGNORECASE, usually written re.I, makes a pattern match regardless of case, so 'robocop' matches "
        "'ROBOCOP' with the flag set. re.DOTALL, re.S, lets the dot match a newline too, which it otherwise never "
        "does, letting a pattern span several printed lines. re.VERBOSE, re.X, lets a pattern be written across "
        "several lines with whitespace and # comments for readability, both ignored when the pattern is compiled "
        "unless the whitespace is escaped or inside a class; this console's own VERBOSE pattern shows the trap, a "
        "comment with no real line break after it quietly eats the rest of the pattern. Flags combine with the "
        "pipe, re.I | re.S | re.X, into one integer passed as the third argument.",
        "re.X comments run to the pattern's own line break, not past it.")

# ---- 17 Project 3: the contact extractor --------------------------------------------------------------------------
p1, bot = prog("contactExtractor_v1_0_0.py", 0.5, 1.5, 9.0, fs=7, lines=(1, 10), show_out=False)
p2 = transcript("contactExtractor_v1_0_0.py", 0.5, bot + 0.2, 9.0, 1.6,
                fs=7, label="prints: the matches found, joined one per line, as the program copies them back")
content("Project 3: extract contact information", "phoneRegex and emailRegex, in VERBOSE mode, find numbers and addresses in a page of text",
        [p1, p2],
        "Project 3 searches a page of text for phone numbers and e-mail addresses with two VERBOSE-mode patterns, "
        "joins the groups of each phone match with hyphens, and copies every match it finds back for the user, "
        "standing in here for the clipboard pyperclip would otherwise reach. The chapter itself prints a real "
        "quirk worth keeping rather than quietly fixing: the extension clause is joined from group 6, the whole "
        "clause including its own 'x' or 'ext', not from group 8, the extension digits alone, so a number with an "
        "extension prints as '415-555-9950 x ext. 123' with the word doubled, and a number with no area code "
        "keeps a stray leading hyphen, '-555-1234'. Running the program here confirms both quirks exactly as the "
        "chapter's own printed transcript shows them.",
        "Project 3's own printed quirk, group 6 not group 8, reruns unchanged.")

# ---- 18 practice: the strong-password check -------------------------------------------------------------------------
p1, bot = prog("strongPasswordDetector_v1_0_0.py", 0.5, 1.5, 9.0, fs=7, lines=(3, 5), show_out=False)
p2 = transcript("strongPasswordDetector_v1_0_0.py", 0.5, bot + 0.4, 9.0, 2.33, fs=7,
                label="typed: password1, PASSWORD1, Password, Sh0rt, then Passw0rdOK, which is accepted")
content("Practice: the strong-password check", "all() over four small patterns: length, a lowercase letter, an uppercase letter, a digit",
        [p1, p2],
        "is_strong_password() holds four small, separate patterns, r'.{8}' for length, r'[a-z]' for a lowercase "
        "letter, r'[A-Z]' for an uppercase letter and r'\\d' for a digit, and all() requires every one of them to "
        "be found somewhere in the password before it is accepted. Typed against password1, PASSWORD1, Password "
        "and Sh0rt, each is rejected for missing exactly one of the four conditions, and Passw0rdOK is accepted the "
        "moment all four are satisfied at once; the loop then breaks rather than asking again. Four short patterns "
        "checked together with all() read far more clearly than one long pattern would have tried to be.",
        "Four short patterns checked with all() replace one long one.")

# ---- 19 practice: regexStrip, and Humre -------------------------------------------------------------------------------
p1 = {**prog("regexStrip_v1_0_0.py", 0.5, 1.5, 4.4, fs=8, show_out=True)[0]}
content("Practice: regex_strip(), and the Humre module", "A pattern rebuilds strip(); Humre writes patterns out as plain-English function calls",
        [p1,
         card("What Humre reproduces", "Humre 1.0.0, the Python Package Index's newest release, reproduces every "
              "row of the chapter's two syntax tables and its phone-number pattern written out as nested function "
              "calls such as group(DIGIT, PERIOD, DIGIT).", 5.1, 1.45, 4.4, 1.65, fs=11),
         card("What differs in Humre 1.0.0", "Several constants are named differently from the chapter (ANYCHAR "
              "for ANY_SINGLE, EVERYTHING for the greedy dot-star, SOMETHING for the lazy dot-plus), and "
              "humre.parse() is an unfinished TODO that returns None rather than generated source; Humre is a "
              "third-party module, not installed for this page.", 5.1, 3.18, 4.4, 1.82, fs=10.5)],
        "regex_strip() rebuilds str.strip() with a pattern: with no character argument it strips leading or "
        "trailing whitespace, r'^\\s+|\\s+$', and with one it builds a character class from the given characters "
        "with re.escape() and strips a run of any of them from either end, which is how strip('xy') removes 'xy' "
        "from both ends of 'xyhixy' down to 'hi'. Humre is a separate, third-party module the chapter introduces "
        "for programmers who find backslash-heavy patterns hard to read, replacing them with chained function "
        "calls that spell out the pattern in English; its newest release reproduces the chapter's own worked "
        "example faithfully but has renamed a few constants and left one function, parse(), unfinished since the "
        "chapter was written, exactly the kind of drift this course checks for rather than assumes away.",
        "Humre reads like English; its own newest release still has gaps.")

# ---- 20 summary ------------------------------------------------------------------------------------------------------
content("The chapter in six lines", "One line for each part of the route",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 11.5, "items": [
            "A hand-written check tests a string by hand; re.compile() then search() replaces it with a pattern.",
            "Parentheses group and number matches; the pipe offers alternatives; (?P<name>...) names a group.",
            "Square brackets name a character set; \\d, \\w and \\s are shorthand for a whole set by name.",
            "?, *, + and {m,n} say how many times; a trailing ? makes any of them take as few as it can.",
            "^, $, \\b and \\B anchor a pattern; a look-around tests text beside a position without consuming it.",
            "findall/finditer find every match; sub() replaces them; flags such as re.I and re.X change the read."]}],
        "These six lines answer the route one part at a time. The first two cover finding a pattern and grouping "
        "what it keeps, the third and fourth cover what one position may be and how many times it repeats, the "
        "fifth covers anchoring a pattern in the text, and the sixth covers doing something with every match. If a "
        "line feels unproven, the part of the route that carries it has the slides with the executed examples.",
        "If a line feels unproven, its slides hold the example.")

# ---- 21 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(":")[0] if r["kind"] != "documentation" or "textbook" not in r["title"].lower() else "The textbook, chapter 9 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


_docs = rows(("documentation",))
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _docs[:3]},
            {"head": "Reference", "rows": _docs[3:]},
            {"head": "History and try it", "rows": [
                ["Stephen Cole Kleene, Wikipedia", STORY["KleeneRegularEvents"]["link"]],
                ["Perl, Wikipedia", STORY["PerlShorthandClasses"]["link"]],
                ["Python's _sre.c source history", STORY["SreBecomesRe"]["link"]]] + rows(("interactive",))}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read "
        "online and has Project 3 and both practice programs in full, the reference links are the official "
        "documentation behind every quirk this deck flagged, and the history links are three of the primary "
        "sources behind this chapter's four stories (Ken Thompson's own 1968 paper is linked from its own story "
        "slide instead, its reference too long to set beside a label here). regex101 and Pythex each let you step "
        "a pattern across real text and watch which part matches, the clearest way to see greedy and lazy "
        "quantifiers disagree.",
        "History, documentation and two testers, opened the day this deck was built.")

# ---- 22 closing -------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "compile() builds a Pattern once; search() returns a Match or None, and never raises on no match.",
            "A pattern's own groups decide findall's shape: a plain list, or a list of tuples once there are two.",
            "Every quantifier is greedy by default; a trailing ? makes it take as few repetitions as it can.",
            "sub()'s replacement can hold \\1 or be a function; flags such as re.I and re.X change how a pattern reads."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d console rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the "
        "examples yourself, you have the chapter. The next chapter moves on to reading, writing and copying files.",
        "Questions are welcome; bring one pattern you could not predict.")

# ---- agenda -----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Finding patterns and pattern objects", "The questions this chapter answers", "A company's own engine, still runs under re"),
          ("Pattern syntax: grouping and character sets", "Grouping: parentheses, the pipe, and names", "\\d, \\w and \\s came from a language, in 1987"),
          ("Pattern syntax: repetition and anchors", "Repetition: quantifiers, greedy and lazy", "Anchors: start, end, word boundary, look-around"),
          ("Pattern operations: finding, replacing, flags", "Finding every match: findall and finditer", "Flags: ignorecase, dotall, verbose, and combined"),
          ("Patterns in programs: Project 3, practice, Humre", "Project 3: extract contact information", "Practice: regex_strip(), and the Humre module"),
          ("Summary and resources", "The chapter in six lines", "Where to go from here")]
_rows = []
for name, a, b in _parts:
    _rows.append("%s (slides %d-%d)" % (name, _t[a], _t[b]))
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 3 or any(_starts[i + 1] != _ends[i] + 1 for i in range(5)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": str(len(ST.STORIES)), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["notes"] = ("The route has six parts. It starts with finding patterns and the Pattern and Match objects, "
                 "moves to pattern syntax for grouping and character sets, then to repetition and anchors, then to "
                 "pattern operations for finding, replacing and flags, then to patterns inside real programs - "
                 "Project 3, the practice programs and Humre - and ends with the summary and resources. The ranges "
                 "name the exact slides, so you can return to the part you need, and four of the slides are true "
                 "stories that explain where a piece of syntax came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 9: Regular Expressions", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
