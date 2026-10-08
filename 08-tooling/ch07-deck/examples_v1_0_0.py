"""Chapter 7 deck examples: every console session, program, chart and table the lecture deck shows.
Nothing here carries a result; examples_run_v1_0_0.py runs it all under the interpreter given and records the results.
A console group is one session: its rows run in order in one namespace (as the deck check re-runs them per slide)."""
__version__ = "1.0.0"
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base7", os.path.join(HERE, "..", "sen0414_ch07_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

CONSOLES = {
    "title": ["{'cat': 'Zophie'}['cat']"],
    "basic": ["my_cat = {'size': 'fat', 'color': 'gray', 'disposition': 'loud'}",
              "my_cat['size']",
              "'My cat has ' + my_cat['color'] + ' fur.'",
              "len(my_cat)"],
    "versus": ["spam = ['cats', 'dogs', 'moose']",
               "bacon = ['moose', 'dogs', 'cats']",
               "spam == bacon",
               "eggs = {'name': 'Zophie', 'species': 'cat', 'age': '8'}",
               "ham = {'age': '8', 'name': 'Zophie', 'species': 'cat'}",
               "eggs == ham",
               "list(ham)"],
    "keys": ["d = {}",
             "d[(1, 2)] = 'a tuple can be a key'",
             "d[[1, 2]] = 'a list cannot'",
             "{1: 'int', 1.0: 'float', True: 'bool'}",
             "hash('cat') == hash('cat')"],
    "read": ["picnic = {'apples': 5, 'cups': 2}",
             "'cups' in picnic",
             "'eggs' not in picnic",
             "picnic.get('eggs', 0)",
             "picnic['eggs']",
             "picnic.setdefault('eggs', 12)",
             "picnic"],
    "change": ["spam = {'color': 'red', 'age': 42}",
               "spam['name'] = 'Pooka'",
               "del spam['age']",
               "spam.pop('color')",
               "spam | {'age': 7}",
               "spam",
               "dict.fromkeys(['a', 'b'], 0)"],
    "counter": ["from collections import Counter",
                "c = Counter('abracadabra')",
                "c.most_common(2)",
                "c['a']",
                "c['z']",
                "sum(c.values())"],
    "model": ["board = {'h1': 'bK', 'c6': 'wQ', 'g2': 'bB', 'h5': 'bQ', 'e3': 'wK'}",
              "'c6' in board",
              "board.get('a1', 'empty')",
              "sorted(board)",
              "len(board)"],
    "notation": ["import json, pprint, typing",
                 "cat = {'name': 'Zophie', 'age': 8}",
                 "json.dumps(cat)",
                 "json.loads('{\"cats\": [1, 2]}')",
                 "pprint.pformat({'b': 1, 'a': 2})",
                 "Cat = typing.TypedDict('Cat', {'name': str, 'age': int})",
                 "type(Cat(name='Zophie', age=8))"],
}

MATCHING = """cat = {'name': 'Zophie', 'age': 8}
match cat:   # keys are tested, values are bound
    case {'name': name, 'age': age} if age > 5:
        print(name, 'is a senior cat of', age)
    case {'name': name}:
        print(name, 'is a cat')
"""

# the book's birthday program as the slide sets it: the same statements, the dictionary on two lines and the comments set close,
# so that the code and its transcript can stand side by side in a readable size
BIRTHDAYS_DECK = """birthdays = {'Alice': 'Apr 1', 'Bob': 'Dec 12',  # name -> birthday
             'Carol': 'Mar 4'}

while True:
    print('Enter a name: (blank to quit)')
    name = input()
    if name == '':
        break

    if name in birthdays:  # is the name one of the keys?
        print(birthdays[name] + ' is the birthday of ' + name)
    else:
        print('I do not have birthday information for ' + name)
        print('What is their birthday?')
        bday = input()
        birthdays[name] = bday  # a new key-value pair
        print('Birthday database updated.')
"""

# name -> (code, stdin text or None)
PROGRAMS = {
    "birthdays_v1_0_0.py": (BIRTHDAYS_DECK, B.BIRTHDAYS_INPUT),
    "loops_v1_0_0.py": (B.LOOPS, None),
    "charcount_short_v1_0_0.py": (B.CHARCOUNT_SHORT, None),
    "grouping_v1_0_0.py": (B.GROUPING, None),
    "chessMoves_v1_0_0.py": (B.CHESS_MOVES, None),
    "guestpicnic_v1_0_0.py": (B.GUEST_PICNIC, None),
    "copying_v1_0_0.py": (B.COPYING, None),
    "matching_v1_0_0.py": (MATCHING, None),
    "inventory_v1_0_0.py": (B.INVENTORY, None),
}

_START = re.search(r"STARTING_PIECES = \{.*?\}", B.CHESSBOARD, re.S).group(0)
_MSG = "message = 'It was a bright cold day in April, and the clocks were striking thirteen.'"
_PIC = B.GUEST_PICNIC.split("\n\ndef")[0]

# name -> (setup statements, expression giving [(label, value), ...])
CHARTS = {
    "letters": (_MSG + "\nfrom collections import Counter",
                "[(repr(k), v) for k, v in Counter(message).most_common(8)]"),
}
# name -> (setup, expression giving a list of rows; row 0 is the header)
TABLES = {
    "board": (_START,
              "[[' '] + list('abcdefgh')] + [[str(r)] + [STARTING_PIECES.get(c + str(r), '') for c in 'abcdefgh'] "
              "for r in range(8, 0, -1)]"),
}
