#!/usr/bin/env python3
"""SEN0414 chapter 7 (Dictionaries and Structuring Data, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds what every text module of the chapter shares: the facet names, the containers RAW / CHECKS / RAISES, the helpers that turn a
whole program into a checkable expression (the chapter 5 helpers, re-written here because a tool of another chapter is not edited),
the chapter's whole programs as text (the single source the corpus checks, the deck, the page's Code Lab and the question bank all
read), and the citation tokens. Nothing in this file is taught text; the paragraphs are in sen0414_ch07_corpus_text_a/b/c_v1_0_0.py.

Sources read for this chapter, on 2026-10-08: the book's chapter (https://automatetheboringstuff.com/3e/chapter7.html, SHA-256 50f4556a...,
equal to the chapterDigest of the textbook ontology); the Python 3.14 documentation (Built-in Types, mapping types dict and dictionary view
objects; The Python Tutorial 5; Data model, object.__hash__; collections; copy; pprint; json; typing; types; Compound statements, mapping
patterns); PEPs 274, 448, 468, 584, 589 and 634. Every behaviour quoted is executed (python3.14 sen0414_ch07_corpus_v1_0_0.py python3.14).
"""
__version__ = "1.0.0"

W, Y, E, H, K, C = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out", "What changed"
CITE = {"[SW]": "(Sweigart, 2025)", "[PSF]": "(Python Software Foundation, 2026)", "[PEP274]": "(Warsaw, 2001)",
        "[PEP448]": "(Landau, 2013)", "[PEP468]": "(Snow, 2014)", "[PEP584]": "(D'Aprano and Bucher, 2019)",
        "[PEP589]": "(Lehtosalo, 2019)", "[PEP634]": "(Bucher and van Rossum, 2020)"}

RAW = []      # the nodes with citation tokens such as [SW] and [PSF]; the main corpus module resolves them
CHECKS = []   # (expression, repr of its value) pairs, all executed
RAISES = []   # (expression, exception class name) pairs, all executed


def PROG(code, expected, stream="stdout", inp=None):
    """a whole program run as a separate process (python -c); the expected text is the stream named"""
    return ("__import__('subprocess').run([__import__('sys').executable, '-c', %r], capture_output=True, text=True, input=%r).%s" % (code, inp, stream), repr(expected))


def PROGF(code, expected, which=1, post="", inp=None):
    """a whole program saved as main.py in a fresh folder and run; which = 0 exit status, 1 standard output, 2 standard error"""
    e = ("(lambda d: (open(d + '/main.py', 'w').write(%r), (lambda r: (r.returncode, r.stdout, r.stderr.replace(d + '/', '')))"
         "(__import__('subprocess').run([__import__('sys').executable, 'main.py'], capture_output=True, text=True, cwd=d, input=%r)))[1])"
         "(__import__('tempfile').mkdtemp())[%d]%s") % (code, inp, which, post)
    return (e, repr(expected))


# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's whole programs. Each is the book's program with comments added (the logic is unchanged); the sample inputs and the
# outputs are produced by running them, never typed.
# ---------------------------------------------------------------------------------------------------------------------------------
BIRTHDAYS = """birthdays = {'Alice': 'Apr 1', 'Bob': 'Dec 12', 'Carol': 'Mar 4'}   # name -> birthday

while True:
    print('Enter a name: (blank to quit)')
    name = input()
    if name == '':
        break

    if name in birthdays:                      # is the name one of the keys?
        print(birthdays[name] + ' is the birthday of ' + name)
    else:
        print('I do not have birthday information for ' + name)
        print('What is their birthday?')
        bday = input()
        birthdays[name] = bday                 # a new key-value pair
        print('Birthday database updated.')
"""
BIRTHDAYS_INPUT = "Alice\nEve\nDec 5\nEve\n\n"
BIRTHDAYS_OUT = ("Enter a name: (blank to quit)\nApr 1 is the birthday of Alice\nEnter a name: (blank to quit)\n"
                 "I do not have birthday information for Eve\nWhat is their birthday?\nBirthday database updated.\n"
                 "Enter a name: (blank to quit)\nDec 5 is the birthday of Eve\nEnter a name: (blank to quit)\n")

CHARACTER_COUNT = """message = 'It was a bright cold day in April, and the clocks were striking thirteen.'
count = {}                                     # character -> how many times it was seen

for character in message:
    count.setdefault(character, 0)             # make sure the key exists, starting at 0
    count[character] = count[character] + 1    # then add one

print(count)
"""
CHARACTER_COUNT_OUT = ("{'I': 1, 't': 6, ' ': 13, 'w': 2, 'a': 4, 's': 3, 'b': 1, 'r': 5, 'i': 6, 'g': 2, 'h': 3, 'c': 3, 'o': 2, "
                       "'l': 3, 'd': 3, 'y': 1, 'n': 4, 'A': 1, 'p': 1, ',': 1, 'e': 5, 'k': 2, '.': 1}\n")

CHARCOUNT_SHORT = """message = 'It was a bright cold day in April, and the clocks were striking thirteen.'
count = {}                                     # character -> how many times it was seen

for character in message:
    count.setdefault(character, 0)             # make sure the key exists, starting at 0
    count[character] = count[character] + 1    # then add one

print(count['c'], count[' '], count['A'])      # the book reads these three off its output
print(len(count), 'different characters in', sum(count.values()), 'characters')
"""

GUEST_PICNIC = """all_guests = {'Alice': {'apples': 5, 'pretzels': 12},
              'Bob': {'ham sandwiches': 3, 'apples': 2},
              'Carol': {'cups': 3, 'apple pies': 1}}

def total_brought(guests, item):
    num_brought = 0
    for k, v in guests.items():                    # k is a guest, v is that guest's dictionary
        num_brought = num_brought + v.get(item, 0)  # 0 when the guest brings none
    return num_brought

print('Number of things being brought:')
print(' - Apples         ' + str(total_brought(all_guests, 'apples')))
print(' - Cups           ' + str(total_brought(all_guests, 'cups')))
print(' - Cakes          ' + str(total_brought(all_guests, 'cakes')))
print(' - Ham Sandwiches ' + str(total_brought(all_guests, 'ham sandwiches')))
print(' - Apple Pies     ' + str(total_brought(all_guests, 'apple pies')))
"""
GUEST_PICNIC_OUT = ("Number of things being brought:\n - Apples         7\n - Cups           3\n - Cakes          0\n"
                    " - Ham Sandwiches 3\n - Apple Pies     1\n")

# the book's interactive chessboard simulator, whole, with comments added
CHESSBOARD = '''import sys, copy

STARTING_PIECES = {'a8': 'bR', 'b8': 'bN', 'c8': 'bB', 'd8': 'bQ',
'e8': 'bK', 'f8': 'bB', 'g8': 'bN', 'h8': 'bR', 'a7': 'bP', 'b7': 'bP',
'c7': 'bP', 'd7': 'bP', 'e7': 'bP', 'f7': 'bP', 'g7': 'bP', 'h7': 'bP',
'a1': 'wR', 'b1': 'wN', 'c1': 'wB', 'd1': 'wQ', 'e1': 'wK', 'f1': 'wB',
'g1': 'wN', 'h1': 'wR', 'a2': 'wP', 'b2': 'wP', 'c2': 'wP', 'd2': 'wP',
'e2': 'wP', 'f2': 'wP', 'g2': 'wP', 'h2': 'wP'}

BOARD_TEMPLATE = """
    a    b    c    d    e    f    g    h
   ____ ____ ____ ____ ____ ____ ____ ____
  ||||||    ||||||    ||||||    ||||||    |
8 ||{}|| {} ||{}|| {} ||{}|| {} ||{}|| {} |
  ||||||____||||||____||||||____||||||____|
  |    ||||||    ||||||    ||||||    ||||||
7 | {} ||{}|| {} ||{}|| {} ||{}|| {} ||{}||
  |____||||||____||||||____||||||____||||||
  ||||||    ||||||    ||||||    ||||||    |
6 ||{}|| {} ||{}|| {} ||{}|| {} ||{}|| {} |
  ||||||____||||||____||||||____||||||____|
  |    ||||||    ||||||    ||||||    ||||||
5 | {} ||{}|| {} ||{}|| {} ||{}|| {} ||{}||
  |____||||||____||||||____||||||____||||||
  ||||||    ||||||    ||||||    ||||||    |
4 ||{}|| {} ||{}|| {} ||{}|| {} ||{}|| {} |
  ||||||____||||||____||||||____||||||____|
  |    ||||||    ||||||    ||||||    ||||||
3 | {} ||{}|| {} ||{}|| {} ||{}|| {} ||{}||
  |____||||||____||||||____||||||____||||||
  ||||||    ||||||    ||||||    ||||||    |
2 ||{}|| {} ||{}|| {} ||{}|| {} ||{}|| {} |
  ||||||____||||||____||||||____||||||____|
  |    ||||||    ||||||    ||||||    ||||||
1 | {} ||{}|| {} ||{}|| {} ||{}|| {} ||{}||
  |____||||||____||||||____||||||____||||||
"""
WHITE_SQUARE = '||'
BLACK_SQUARE = '  '

def print_chessboard(board):
    squares = []                               # 64 strings, one for each {} in the template
    is_white_square = True
    for y in '87654321':
        for x in 'abcdefgh':
            if x + y in board.keys():          # a key means a piece stands on that square
                squares.append(board[x + y])
            else:                              # no key means the square is empty
                if is_white_square:
                    squares.append(WHITE_SQUARE)
                else:
                    squares.append(BLACK_SQUARE)
            is_white_square = not is_white_square
        is_white_square = not is_white_square

    print(BOARD_TEMPLATE.format(*squares))     # the star passes the 64 strings one by one

print('Interactive Chessboard')
print('by Al Sweigart al@inventwithpython.com')
print()
print('Pieces:')
print('  w - White, b - Black')
print('  P - Pawn, N - Knight, B - Bishop, R - Rook, Q - Queen, K - King')
print('Commands:')
print('  move e2 e4 - Moves the piece at e2 to e4')
print('  remove e2 - Removes the piece at e2')
print('  set e2 wP - Sets square e2 to a white pawn')
print('  reset - Resets pieces back to their starting squares')
print('  clear - Clears the entire board')
print('  fill wP - Fills entire board with white pawns.')
print('  quit - Quits the program')

main_board = copy.copy(STARTING_PIECES)
while True:
    print_chessboard(main_board)
    response = input('> ').split()

    if response[0] == 'move':
        main_board[response[2]] = main_board[response[1]]
        del main_board[response[1]]
    elif response[0] == 'remove':
        del main_board[response[1]]
    elif response[0] == 'set':
        main_board[response[1]] = response[2]
    elif response[0] == 'reset':
        main_board = copy.copy(STARTING_PIECES)
    elif response[0] == 'clear':
        main_board = {}
    elif response[0] == 'fill':
        for y in '87654321':
            for x in 'abcdefgh':
                main_board[x + y] = response[1]
    elif response[0] == 'quit':
        sys.exit()
'''

# the deck's own readable drive of the same commands: the dictionary only, no template
CHESS_MOVES = """import copy

STARTING_PIECES = {'a1': 'wR', 'e1': 'wK', 'e2': 'wP', 'd7': 'bP', 'e8': 'bK', 'h8': 'bR'}   # a small start position
board = copy.copy(STARTING_PIECES)             # a copy, so STARTING_PIECES stays intact

board['e4'] = board['e2']                      # move e2 e4: copy the piece to the new key ...
del board['e2']                                #             ... then delete the old key
print('after move e2 e4:', sorted(board))

del board['d7']                                # remove d7
board['d5'] = 'wP'                             # set d5 wP
print('after remove and set:', sorted(board))

board = copy.copy(STARTING_PIECES)             # reset
print('after reset:', len(board), 'pieces, e2 holds', board['e2'])
board = {}                                     # clear
print('after clear:', len(board), 'pieces')
"""

INVENTORY = """stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def display_inventory(inventory):
    print('Inventory:')
    item_total = 0
    for k, v in inventory.items():             # key: the item, value: how many
        print(str(v) + ' ' + k)
        item_total = item_total + v
    print('Total number of items: ' + str(item_total))

def add_to_inventory(inventory, added_items):
    for item in added_items:                   # the loot is a list and may repeat an item
        inventory.setdefault(item, 0)          # a new item starts at 0 ...
        inventory[item] = inventory[item] + 1  # ... and every sighting adds one
    return inventory

display_inventory(stuff)
print()
inv = {'gold coin': 42, 'rope': 1}
dragon_loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = add_to_inventory(inv, dragon_loot)
display_inventory(inv)
"""
INVENTORY_OUT = ("Inventory:\n1 rope\n6 torch\n42 gold coin\n1 dagger\n12 arrow\nTotal number of items: 62\n\n"
                 "Inventory:\n45 gold coin\n1 rope\n1 dagger\n1 ruby\nTotal number of items: 48\n")

VALIDATOR = """def is_valid_chessboard(board):
    kinds = {'P': 'pawn', 'N': 'knight', 'B': 'bishop', 'R': 'rook', 'Q': 'queen', 'K': 'king'}
    count = {}                                 # piece string -> how many stand on the board
    for square, piece in board.items():
        if len(square) != 2 or square[0] not in 'abcdefgh' or square[1] not in '12345678':
            return False                       # the key is not a square from a1 to h8
        if len(piece) != 2 or piece[0] not in 'wb' or piece[1] not in kinds:
            return False                       # the value is not a colour letter and a piece letter
        count[piece] = count.get(piece, 0) + 1
    for colour in 'wb':
        if count.get(colour + 'K', 0) != 1:    # exactly one king of each colour
            return False
        if count.get(colour + 'P', 0) > 8:     # at most eight pawns
            return False
        if sum(n for p, n in count.items() if p[0] == colour) > 16:
            return False                       # at most sixteen pieces
    return True

book_board = {'h1': 'bK', 'c6': 'wQ', 'g2': 'bB', 'h5': 'bQ', 'e3': 'wK'}
print(is_valid_chessboard(book_board))
print(is_valid_chessboard({**book_board, 'a1': 'wK'}))      # a second white king
print(is_valid_chessboard({**book_board, 'i9': 'wP'}))      # a square that does not exist
print(is_valid_chessboard({**book_board, **{c + '2': 'wP' for c in 'abcdefghi'[:8]}, 'a3': 'wP'}))   # nine white pawns
"""
VALIDATOR_OUT = "True\nFalse\nFalse\nFalse\n"

# small programs that carry one idea each (used by the deck and by the page's Code Lab)
LOOKUP = """picnic_items = {'apples': 5, 'cups': 2}
print('I am bringing ' + str(picnic_items.get('cups', 0)) + ' cups.')
print('I am bringing ' + str(picnic_items.get('eggs', 0)) + ' eggs.')
print('eggs' in picnic_items)                  # get() did not add the key
try:
    print('I am bringing ' + str(picnic_items['eggs']) + ' eggs.')
except KeyError as e:
    print('KeyError:', e)
"""
LOOKUP_OUT = "I am bringing 2 cups.\nI am bringing 0 eggs.\nFalse\nKeyError: 'eggs'\n"

LOOPS = """spam = {'color': 'red', 'age': 42}
for k, v in spam.items():                      # each pass unpacks one (key, value) tuple
    print('Key: ' + str(k) + ' Value: ' + str(v))
keys = spam.keys()                             # a view, not a copy
spam['name'] = 'Pooka'
print(list(keys))                              # the view shows the later change
print(sorted(spam))                            # a sorted list of the keys
print(list(reversed(spam)))                    # newest key first
"""
LOOPS_OUT = "Key: color Value: red\nKey: age Value: 42\n['color', 'age', 'name']\n['age', 'color', 'name']\n['name', 'age', 'color']\n"

GROUPING = """words = ['apple', 'avocado', 'banana', 'blueberry', 'cherry', 'apricot']
groups = {}                                    # first letter -> list of words
for word in words:
    groups.setdefault(word[0], []).append(word)   # create the list once, then append
for letter, found in groups.items():
    print(letter, found)

from collections import defaultdict
same = defaultdict(list)                       # the same job, the missing key creates its list
for word in words:
    same[word[0]].append(word)
print(dict(same) == groups)
"""
GROUPING_OUT = ("a ['apple', 'avocado', 'apricot']\nb ['banana', 'blueberry']\nc ['cherry']\nTrue\n")

COPYING = """import copy

original = {'Alice': {'apples': 5}, 'Bob': {'apples': 2}}
alias = original                               # no copy at all: a second name
shallow = copy.copy(original)                  # a new outer dictionary, the same inner ones
deep = copy.deepcopy(original)                 # new at every level

original['Alice']['apples'] = 99               # change an inner dictionary
print(alias['Alice']['apples'])
print(shallow['Alice']['apples'])
print(deep['Alice']['apples'])
print(shallow['Alice'] is original['Alice'], deep['Alice'] is original['Alice'])
"""
COPYING_OUT = "99\n99\n5\nTrue False\n"

PROGRAMS = {
    "birthdays_v1_0_0.py": (BIRTHDAYS, BIRTHDAYS_INPUT, BIRTHDAYS_OUT),
    "characterCount_v1_0_0.py": (CHARACTER_COUNT, None, CHARACTER_COUNT_OUT),
    "guestpicnic_v1_0_0.py": (GUEST_PICNIC, None, GUEST_PICNIC_OUT),
    "inventory_v1_0_0.py": (INVENTORY, None, INVENTORY_OUT),
    "validator_v1_0_0.py": (VALIDATOR, None, VALIDATOR_OUT),
    "lookup_v1_0_0.py": (LOOKUP, None, LOOKUP_OUT),
    "loops_v1_0_0.py": (LOOPS, None, LOOPS_OUT),
    "grouping_v1_0_0.py": (GROUPING, None, GROUPING_OUT),
    "copying_v1_0_0.py": (COPYING, None, COPYING_OUT),
}
