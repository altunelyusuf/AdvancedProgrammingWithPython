#!/usr/bin/env python3
"""Chapter 7 deck v2.0.0 - the code examples, in slide order, as ONE source of truth (a NEW tool file; the v1.0.0 files are untouched).

Each example is a list of line groups; a group is (code lines, a plain-language note). The deck shows each group in its own code box with the
note beside it; the page's chapter-code tab lists the same examples by NAME in the same order (chapter_code_ch07_v1_0_0.json); the result shown on a
slide is what this file's runner PRINTS when the example is executed under Python 3.14. Nothing on a slide's result is typed: it is read from the run.

Rules the examples obey (so that the deck standard D2, D3 and D12 can be met and the page can run them):
  * every code box holds at most 30 words (the standard's limit for a text box), so a group is two to four short lines;
  * no code line is longer than MAXLINE characters, so that no line wraps;
  * every example is self-contained, uses only the standard library, needs no keyboard and prints nothing that depends on the interpreter's version.

Usage: examples_v2_0_0.py   (runs every example, prints the output, exits 1 on any error, long line or box over 30 words)"""
__version__ = "2.0.0"
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("PY314", "/root/.local/bin/python3.14")
MAXLINE = 56
MAXWORDS = 30

PRELUDE = ""   # every example is self-contained: nothing is defined for it beforehand

EXAMPLES = [
    dict(id="dict_basics", name="A dictionary holds key-value pairs", sub="Braces hold the pairs; a key finds its value",
         src="The Dictionary Data Type", concepts=["dictionary", "key", "value", "key-value pair"], watch=["my_cat"],
         groups=[
             (["my_cat = {'size': 'fat', 'color': 'gray', 'age': 8}", "print(my_cat['size'])"],
              "Braces hold three pairs. The key 'size' finds its value, 'fat', directly."),
             (["print('My cat has ' + my_cat['color'] + ' fur.')", "print(len(my_cat))"],
              "A value can be used like any text. len() counts the pairs, not the characters."),
         ],
         take="A key finds its value; the position of the pair does not matter.",
         notes="A dictionary is a collection of key-value pairs between braces. You ask by key and the value comes back at once, however many pairs there are. len() counts the pairs."),
    dict(id="dict_vs_list", name="Dictionaries versus lists", sub="Two containers, two ways to name an item",
         src="Comparing Dictionaries and Lists", concepts=["Comparing Dictionaries and Lists"], watch=[],
         groups=[
             (["spam = ['cats', 'dogs', 'moose']", "bacon = ['moose', 'dogs', 'cats']", "print(spam == bacon)"],
              "Two lists with the same items in another order are not equal."),
             (["eggs = {'name': 'Zophie', 'age': 8, 'species': 'cat'}", "ham = {'age': 8, 'species': 'cat', 'name': 'Zophie'}", "print(eggs == ham)"],
              "Two dictionaries with the same pairs are equal, whatever the order."),
             (["print(list(ham))"],
              "Yet the dictionary still remembers the order in which its keys were added."),
         ],
         take="Lists compare by position; dictionaries compare by pairs.",
         notes="A list names its items by position, so order matters for equality. A dictionary names them by key, so two dictionaries with the same pairs are equal. Insertion order is still kept and shown by list()."),
    dict(id="insertion_order", name="Dictionaries remember insertion order", sub="Since Python 3.7 the order of adding is a promise",
         src="The Dictionary Data Type", concepts=["dictionary"], watch=[],
         groups=[
             (["d = {}", "d['pear'] = 3", "d['apple'] = 5", "d['fig'] = 1"],
              "Add three pairs one after another: pear, apple, fig."),
             (["print(list(d))", "print(d == {'fig': 1, 'pear': 3, 'apple': 5})"],
              "Loops and list() follow the order of adding. Equality ignores the order."),
             (["del d['pear']", "d['pear'] = 9", "print(list(d))"],
              "A key removed and added again joins the end of the line."),
         ],
         take="Keys come back in the order they were added; equality does not care.",
         notes="The chapter says a dictionary has no first item. That was true of old Python. Since 3.7 the language guarantees that keys keep the order in which they were added, and a re-added key goes to the end."),
    dict(id="hashable_keys", name="Keys must be hashable", sub="A key has to be a value that never changes",
         src="The Dictionary Data Type", concepts=["unhashable type", "key"], watch=[],
         groups=[
             (["d = {}", "d[(1, 2)] = 'a tuple works'", "print(d)"],
              "A tuple of numbers never changes, so it can be a key."),
             (["try:", "    d[[1, 2]] = 'a list fails'", "except TypeError as e:", "    print(type(e).__name__)"],
              "A list can change, so it is unhashable and refused with a TypeError."),
             (["print({1: 'int', 1.0: 'float', True: 'bool'})"],
              "The numbers 1, 1.0 and True are equal and hash alike, so they are one key."),
         ],
         take="A key must never change, so tuples are welcome and lists are not.",
         notes="Python files each key by its hash, a number that must never change while the key is in the dictionary. Lists, sets and dictionaries can change, so they are unhashable and cannot be keys. Equal numbers share one key."),
    dict(id="keys_values_items", name="Reading keys, values and items", sub="Three methods return the parts of a dictionary",
         src="Returning Keys and Values", concepts=["keys", "values", "items", "Returning Keys and Values"], watch=[],
         groups=[
             (["spam = {'color': 'red', 'age': 42}", "print(list(spam.keys()))", "print(list(spam.values()))"],
              "keys() gives the keys and values() the values; list() makes them printable."),
             (["for k, v in spam.items():", "    print(k, '->', v)"],
              "items() hands over one (key, value) pair on each turn of the loop."),
             (["print(list(spam.items()))"],
              "Each pair is a tuple that holds the key first and then the value."),
         ],
         take="keys() for the labels, values() for the contents, items() for both.",
         notes="The three methods return views, not lists. Wrapping them in list() makes them printable. items() is the one you use in loops, because it gives the key and the value together."),
    dict(id="key_exists", name="Checking whether a key exists", sub="Test first, or ask with a fallback",
         src="Checking Whether a Key Exists", concepts=["Checking Whether a Key Exists", "get"], watch=[],
         groups=[
             (["picnic = {'apples': 5, 'cups': 2}", "print('cups' in picnic)", "print('eggs' not in picnic)"],
              "in asks about keys, not values. Both tests answer True or False."),
             (["print(picnic.get('eggs', 0))", "print(picnic.get('cups', 0))"],
              "get() returns the value, or your fallback when the key is missing."),
             (["try:", "    picnic['eggs']", "except KeyError as e:", "    print('KeyError', e)"],
              "Square brackets on a missing key raise a KeyError that names the key."),
         ],
         take="Use get() when a missing key is normal, and brackets when it is a bug.",
         notes="Brackets on a missing key raise a KeyError. The in test and get() do not, so they suit data where a key may be absent. get() lets you choose the fallback value."),
    dict(id="setdefault", name="Setting default values with setdefault", sub="Add the pair only when the key is missing",
         src="Setting Default Values", concepts=["Setting Default Values", "setdefault"], watch=["picnic"],
         groups=[
             (["picnic = {'apples': 5, 'cups': 2}", "print(picnic.setdefault('eggs', 12))"],
              "setdefault() adds the pair only when the key is missing, and returns the value."),
             (["print(picnic.setdefault('eggs', 99))", "print(picnic)"],
              "The second call finds 'eggs' and leaves it alone, so 99 is never used."),
         ],
         take="setdefault() sets a value once and then leaves it alone.",
         notes="setdefault() does two jobs in one call. If the key is missing it stores your default; either way it returns the value now in the dictionary. That makes counting and grouping short."),
    dict(id="change_pairs", name="Adding, removing and merging pairs", sub="Assign, del, pop and the | operator",
         src="The Dictionary Data Type", concepts=["del"], watch=[],
         groups=[
             (["spam = {'color': 'red', 'age': 42}", "spam['name'] = 'Pooka'", "del spam['age']"],
              "Assignment adds a pair; del removes one. A missing key in del raises a KeyError."),
             (["print(spam.pop('color'))", "print(spam)"],
              "pop() removes a pair and hands its value back to you."),
             (["print(spam | {'name': 'Rex', 'legs': 4})", "print(spam)"],
              "The | operator builds a new dictionary; the right-hand value wins. spam is unchanged."),
         ],
         take="Assignment adds or replaces, del and pop remove, and | merges into a new dictionary.",
         notes="Assignment adds a pair or replaces its value. del removes by key and pop also returns the value. The merge operator arrived in Python 3.9 and builds a new dictionary instead of changing either one."),
    dict(id="views_follow", name="Views follow the dictionary", sub="A view is a window; list() is a photograph",
         src="Returning Keys and Values", concepts=["list()"], watch=[],
         groups=[
             (["stock = {'pear': 3, 'apple': 5}", "ks = stock.keys()", "frozen = list(stock)"],
              "A view is a live window; list() takes a photograph of the keys right now."),
             (["stock['fig'] = 1", "print(list(ks))", "print(frozen)"],
              "After a change the window shows 'fig', but the photograph does not."),
             (["print(sorted(stock))", "print(list(reversed(stock)))"],
              "sorted() returns a new sorted list; reversed() walks the newest key first."),
         ],
         take="A view follows the dictionary; list() and sorted() freeze it.",
         notes="keys(), values() and items() return views that show later changes. list() copies the keys at one moment. sorted() returns a new sorted list, and reversed() walks the keys from the newest."),
    dict(id="birthdays", name="birthdays.py with the typing scripted", sub="One in test chooses between a lookup and a new pair",
         src="birthdays.py", concepts=["birthdays.py", "input()", "sys.exit()"], watch=["birthdays"],
         groups=[
             (["birthdays = {'Alice': 'Apr 1', 'Bob': 'Dec 12'}", "typed = iter(['Alice', 'Eve', 'Dec 5', 'Eve', ''])"],
              "The names and dates a person would type are scripted in a list."),
             (["while (name := next(typed)) != '':", "    if name in birthdays:", "        print(name, 'has birthday', birthdays[name])"],
              "Read a name; an empty name ends the loop. A known name prints its date."),
             (["    else:", "        birthdays[name] = next(typed)", "        print('Learned', name, birthdays[name])"],
              "An unknown name takes the next typed line as its date and is stored."),
         ],
         take="One in test and one assignment make a program that learns.",
         notes="The book's program asks with input() and leaves the loop with break; sys.exit() would end the whole program. Here a scripted list stands in for the keyboard so that the run is repeatable."),
    dict(id="char_count", name="characterCount.py counts every character", sub="setdefault() starts each count at 0, then one is added",
         src="characterCount.py", concepts=["characterCount.py"], watch=["count"],
         groups=[
             (["message = ('It was a bright cold day in April, '", "           'and the clocks were striking thirteen.')"],
              "The first sentence of a famous novel is the text to count."),
             (["count = {}", "for ch in message:", "    count.setdefault(ch, 0)", "    count[ch] += 1"],
              "setdefault() starts a new character at 0; then one is added per sighting."),
             (["top = sorted(count.items(), key=lambda kv: -kv[1])[:8]", "print(top)", "print(sum(count.values()), len(count))"],
              "Sort the pairs by count, biggest first. Then total the counts and count the keys."),
         ],
         take="Counting by key turns any text into a table of totals.",
         notes="Each character is a key and its count is the value. setdefault() makes sure the key exists before one is added. The chart shows the eight most frequent characters of the sentence."),
    dict(id="counter", name="Counter does the counting", sub="One call replaces the whole counting loop",
         src="Setting Default Values", concepts=[], watch=["c"],
         groups=[
             (["from collections import Counter", "c = Counter('abracadabra')", "print(c.most_common(2))"],
              "Counter builds the table of counts in one call. most_common() lists the leaders."),
             (["print(c['a'], c['z'])", "print(sum(c.values()))", "print(dict(c))"],
              "A missing key counts as 0 and is not added. The counts add up to the text length."),
         ],
         take="Counter counts in one call, and a missing key simply counts as zero.",
         notes="Counter is a dictionary built for counting. It does by itself what the setdefault loop did. A key that was never seen answers 0 without being added."),
    dict(id="grouping", name="Grouping with setdefault and defaultdict", sub="Each item is slipped into the list for its first letter",
         src="Setting Default Values", concepts=["setdefault"], watch=["groups"],
         groups=[
             (["words = ['ant', 'ape', 'bee', 'bat', 'cat']", "groups = {}"],
              "Five words to sort by their first letter, and an empty dictionary to fill."),
             (["for w in words:", "    groups.setdefault(w[0], []).append(w)", "print(groups)"],
              "setdefault() creates the list for a letter once; append() then adds the word."),
             (["from collections import defaultdict", "g2 = defaultdict(list)", "for w in words:", "    g2[w[0]].append(w)", "print(g2 == groups)"],
              "defaultdict(list) creates the missing list by itself, with the same result."),
         ],
         take="setdefault() and defaultdict both create the missing list for you.",
         notes="Grouping is counting with lists instead of numbers. The first letter is the key and the list of words is the value. defaultdict(list) builds the empty list automatically, so the loop gets shorter."),
    dict(id="board_model", name="Modelling a chessboard", sub="A square is a key; the piece is the value",
         src="Model Real-World Things Using Data Structures", concepts=["data structure", "data model", "Model Real-World Things Using Data Structures"], watch=["board"],
         groups=[
             (["board = {'h1': 'bK', 'c6': 'wQ', 'g2': 'bB',", "         'h5': 'bQ', 'e3': 'wK'}"],
              "Each occupied square is a key; the piece is its value, a colour letter then a piece letter."),
             (["print('c6' in board, board.get('a1', 'empty'))", "print(sorted(board), len(board))"],
              "Ask about squares: c6 is occupied, a1 is empty, and only five keys exist."),
         ],
         take="A good model stores only what is there.",
         notes="This is the board of the book's Figure 7-2. Only occupied squares are keys, so an empty square is simply absent. The model keeps the data apart from how it is drawn."),
    dict(id="board_print", name="Printing the board from the dictionary", sub="The dictionary is the data; the printout is one view",
         src="chessboard.py", concepts=["chessboard.py"], watch=[],
         groups=[
             (["board = {'a1': 'wR', 'e1': 'wK', 'e8': 'bK'}", "files = 'abcdefgh'", "for r in range(8, 0, -1):"],
              "A small position. Walk the ranks from 8 down to 1, as a chess diagram is drawn."),
             (["    row = [board.get(f + str(r), '..') for f in files]", "    print(r, ' '.join(row))"],
              "Look up every square of the rank; an empty square prints as two dots."),
         ],
         take="The same dictionary can be drawn in any way you like.",
         notes="The printing code never changes the dictionary. For each rank it looks up eight squares with get() and a fallback of two dots. The table shows the printed lines as a board."),
    dict(id="chess_moves", name="Chess commands are dictionary operations", sub="Moving a piece is copy-then-delete",
         src="Project 1: Interactive Chessboard Simulator", concepts=["Project 1: Interactive Chessboard Simulator", "copy.copy()", "format"], watch=["board", "START"],
         groups=[
             (["import copy", "START = {'a1': 'wR', 'e1': 'wK', 'e2': 'wP'}", "board = copy.copy(START)"],
              "Keep the starting position safe and play on a copy of it."),
             (["board['e4'] = board['e2']", "del board['e2']", "print('{} moves {} to {}'.format('wP', 'e2', 'e4'))"],
              "A move copies the piece to the new square, deletes the old one, and reports it."),
             (["print(sorted(board))", "print(sorted(START))"],
              "The board changed; the starting position did not."),
         ],
         take="Every simulator command is one or two dictionary operations.",
         notes="The simulator's move command is an assignment followed by del. format() builds the sentence that reports the move. copy.copy() makes sure that START is still intact afterwards."),
    dict(id="validator", name="A chess dictionary validator", sub="Every rule becomes a check on keys or values",
         src="Chess Dictionary Validator", concepts=["Chess Dictionary Validator"], watch=[],
         groups=[
             (["squares = {f + r for f in 'abcdefgh'", "           for r in '12345678'}"],
              "Build the set of all 64 legal square names, a1 to h8."),
             (["board = {'e1': 'wK', 'e8': 'bK', 'z9': 'wQ'}", "bad = [s for s in board if s not in squares]"],
              "A position with one impossible square, z9. List every key that is not a square."),
             (["kings = sorted(p for p in board.values() if p[1] == 'K')", "print(bad, kings, kings == ['bK', 'wK'])"],
              "Collect the kings from the values. A legal position has exactly one king of each colour."),
         ],
         take="A validator turns each rule of the game into a test on keys or values.",
         notes="The first rule looks at the keys: each must be a real square. The second looks at the values: one white king and one black king. The shortened validator shows the idea of the chapter's practice program."),
    dict(id="picnic_nested", name="Nested dictionaries: the picnic", sub="A dictionary inside a dictionary holds a record inside a record",
         src="Nested Dictionaries and Lists", concepts=["Nested Dictionaries and Lists", "guestpicnic.py"], watch=["guests"],
         groups=[
             (["guests = {'Alice': {'apples': 5, 'pretzels': 12},", "          'Bob': {'apples': 2, 'ham sandwiches': 3}}"],
              "Each guest is a key; the value is another dictionary of what they brought."),
             (["def total(item):", "    return sum(v.get(item, 0) for v in guests.values())"],
              "Add up one item over all guests; get() gives 0 for a guest who did not bring it."),
             (["print(total('apples'), total('cups'))", "print(guests['Alice']['pretzels'])"],
              "Two keys in a row reach the inner value. Nobody brought cups, so the total is 0."),
         ],
         take="get() with a default keeps the picnic totals honest.",
         notes="The outer dictionary maps a guest to an inner dictionary. Two brackets reach an inner value. get() with 0 avoids a KeyError for guests who did not bring an item."),
    dict(id="inventory", name="Fantasy game inventory", sub="Display a dictionary of items and total them",
         src="Fantasy Game Inventory", concepts=["Fantasy Game Inventory"], watch=["stuff"],
         groups=[
             (["stuff = {'rope': 1, 'torch': 6, 'gold coin': 42}", "total = 0"],
              "The inventory maps each item to how many the player carries."),
             (["for k, v in stuff.items():", "    print(str(v) + ' ' + k)", "    total += v"],
              "Print each item with its count, and add the count to a running total."),
             (["print('Total number of items:', total)"],
              "The total is the sum of the values, not the number of keys."),
         ],
         take="Each practice program reads a dictionary and applies a rule.",
         notes="This is the display function of the inventory practice program. items() gives the item and its count, and the running total adds the counts. The chart draws the same dictionary."),
    dict(id="loot", name="List-to-dictionary loot conversion", sub="A list of loot is added into the inventory",
         src="List-to-Dictionary Loot Conversion", concepts=["List-to-Dictionary Loot Conversion"], watch=["inv"],
         groups=[
             (["loot = ['gold coin', 'dagger', 'gold coin', 'ruby']", "inv = {'gold coin': 42, 'rope': 1}"],
              "A list of loot from the dragon, and the inventory so far."),
             (["for item in loot:", "    inv[item] = inv.get(item, 0) + 1"],
              "For every piece of loot, read the current count (0 if new) and add one."),
             (["print(inv)", "print(sum(inv.values()))"],
              "Gold coin grew to 44, and two new items joined. Forty-seven items in all."),
         ],
         take="get(item, 0) + 1 turns any list into counts.",
         notes="The loop looks up each item with get() and a default of 0, adds one and stores it back. Known items grow and new items appear. The chart shows the resulting inventory."),
    dict(id="copies", name="Alias, shallow copy and deep copy", sub="Changing an inner dictionary shows which copies share it",
         src="Nested Dictionaries and Lists", concepts=["copy.copy()"], watch=[],
         groups=[
             (["import copy", "original = {'Alice': {'apples': 5}}", "alias = original"],
              "An alias is only a second name for the same dictionary."),
             (["shallow = copy.copy(original)", "deep = copy.deepcopy(original)"],
              "copy() copies the outside only; deepcopy() copies everything inside as well."),
             (["original['Alice']['apples'] = 99", "apples = lambda c: c['Alice']['apples']", "print(apples(alias), apples(shallow), apples(deep))"],
              "Change the inner dictionary through the original, then ask the three others."),
             (["print(alias is original, shallow is original)", "print(shallow['Alice'] is original['Alice'])"],
              "A shallow copy is a new outer dictionary that still shares the inner ones."),
         ],
         take="A shallow copy shares the inner dictionaries; deepcopy does not.",
         notes="The alias is the same object, so it sees every change. The shallow copy has its own outer dictionary but shares the inner ones, so it sees the change too. Only deepcopy is independent."),
    dict(id="json_pprint", name="Writing data down with json and pprint", sub="Text carries a dictionary out of a program and back",
         src="Nested Dictionaries and Lists", concepts=[], watch=[],
         groups=[
             (["import json, pprint", "cat = {'name': 'Zophie', 'toys': ['ball', 'mouse']}", "text = json.dumps(cat)"],
              "dumps() turns the dictionary into text; the text could be saved in a file."),
             (["print(text)", "print(json.loads(text) == cat)"],
              "loads() turns the text back into an equal dictionary."),
             (["pprint.pprint({'b': [1, 2], 'a': {'x': 1}}, width=20)"],
              "pprint() lays nested data out tidily, one key to a line, sorted by key."),
         ],
         take="JSON is how a dictionary leaves a program and comes back.",
         notes="JSON is plain text built from the same pieces as a dictionary: pairs and lists. dumps() writes it and loads() reads it back. pprint is for people reading nested data, not for storing it."),
    dict(id="typed_records", name="Typed records and read-only views", sub="Naming the keys of a dictionary for the type checker",
         src="Nested Dictionaries and Lists", concepts=[], watch=[],
         groups=[
             (["from typing import TypedDict", "class Cat(TypedDict):", "    name: str", "    age: int"],
              "A TypedDict names the keys of a record and the type of each value."),
             (["c = Cat(name='Zophie', age=8)", "print(type(c).__name__, c['age'])"],
              "At run time it is an ordinary dict; only a type checker enforces the keys."),
             (["from types import MappingProxyType", "ro = MappingProxyType(c)", "print(ro['age'], len(ro))"],
              "MappingProxyType gives a read-only view of the same dictionary."),
         ],
         take="TypedDict is checked by type checkers only; at run time it is a plain dict.",
         notes="A TypedDict documents what keys a record has, but Python does not enforce it while running. MappingProxyType is a read-only window onto a dictionary, which stops accidental changes."),
    dict(id="match_dict", name="Matching the shape of a dictionary", sub="Keys are tested and values are bound",
         src="Nested Dictionaries and Lists", concepts=[], watch=[],
         groups=[
             (["cat = {'name': 'Zophie', 'age': 8}"],
              "A record with two keys: a name and an age, ready to be matched."),
             (["match cat:", "    case {'name': n, 'age': a} if a > 5:", "        print(n, 'is a senior cat of', a)", "    case {'name': n}:", "        print(n, 'is a cat')"],
              "The first case needs both keys and an age above 5; otherwise the second case is tried."),
         ],
         take="match tests which keys a dictionary has and binds their values.",
         notes="A mapping pattern checks that the keys exist and binds the values to names. Extra keys are allowed. The first case that fits wins, and a guard such as a > 5 can refuse it."),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_text(ex):
    return "\n".join(l for g, _ in ex["groups"] for l in g)


def box_words(lines):
    return sum(len((">>> " + l).split()) for l in lines)


RUNNER = r'''
import sys, io, json, contextlib
ns = {"__name__": "__main__"}
exec(%(prelude)r, ns)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(%(code)r, ns)
print(json.dumps({"out": buf.getvalue(), "vars": {k: repr(ns[k]) for k in %(watch)r}}))
'''


def run(ex, timeout=60):
    src = RUNNER % dict(prelude=PRELUDE, code=code_text(ex), watch=ex["watch"])
    r = subprocess.run([PY, "-B", "-I", "-c", src], capture_output=True, text=True, timeout=timeout, cwd="/")
    if r.returncode:
        raise SystemExit("EXAMPLE %s FAILED: %s" % (ex["id"], r.stderr.strip()[-600:]))
    return json.loads(r.stdout)


def run_all():
    return {ex["id"]: run(ex) for ex in EXAMPLES}


def lint():
    bad = []
    for ex in EXAMPLES:
        for g, note in ex["groups"]:
            for l in g:
                if len(l) > MAXLINE:
                    bad.append("LONG LINE (%d) in %s: %s" % (len(l), ex["id"], l))
            if box_words(g) > MAXWORDS:
                bad.append("BOX OVER %d WORDS (%d) in %s: %s" % (MAXWORDS, box_words(g), ex["id"], g[0]))
            if len(note.split()) < 8 and len(g) > 0 and note:
                pass
        for _, note in ex["groups"]:
            if len(note.split()) > 30:
                bad.append("NOTE OVER 30 WORDS in %s" % ex["id"])
        if len(ex["notes"].split()) > 60:
            bad.append("SPEAKER NOTE OVER 60 WORDS in %s" % ex["id"])
        if len(ex["take"].split()) > 24:
            bad.append("TAKEAWAY OVER 24 WORDS in %s" % ex["id"])
    return bad


if __name__ == "__main__":
    bad = lint()
    for b in bad:
        print(b)
    for ex in EXAMPLES:
        r = run(ex)
        print("==", ex["id"], "|", ex["name"]); print(r["out"], end="")
        if r["vars"]:
            print("   vars:", r["vars"])
    sys.exit(1 if bad else 0)
