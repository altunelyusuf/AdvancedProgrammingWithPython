#!/usr/bin/env python3
"""Writes question_bank_v1_1_0.json for SEN0414 chapter 7 (version 1.1.0 because ch07-page already holds an older question_bank_v1_0_0.json,
which is not edited). Every concept (leaf, section and branch) gets an Understand item; every leaf also gets an Apply item with a
program. The correct option of an Apply item is NOT typed here: it is the output of the program, run under python3.14 by this script,
and the wrong options are typed. The position of the correct option cycles over 0..3 over all items, so the four positions each carry
a quarter of the bank. The bank is then checked by question_bank_check_v1_2_0.py (run on the finished page data)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import sen0414_ch07_corpus_v1_0_0 as C

# (concept, Understand question, right, [3 wrong], why, Apply program, [3 wrong outputs])
LEAF = [
("DictionaryType", "How does a dictionary find the value for 'color' in my_cat = {'size': 'fat', 'color': 'gray', 'age': 17}?",
 "By the key 'color', which names the value directly", ["By counting to position 1 in the order the pairs were typed", "By searching every value for the text 'color'", "By sorting the pairs and taking the middle one"],
 "A dictionary joins each key to a value, and the key in square brackets selects the value in the way an index selects an item of a list.",
 "my_cat = {'size': 'fat', 'color': 'gray', 'age': 17}\nprint('My cat has ' + my_cat['color'] + ' fur.')", ["My cat has fat fur.", "My cat has color fur.", "My cat has 17 fur."]),
("KeyValuePair", "In {'color': 'red', 'age': 42}, which of these is exactly one key-value pair?",
 "The key 'age' together with its value 42", ["The two keys 'color' and 'age' together", "The two values 'red' and 42 together", "The whole dictionary between the curly brackets"],
 "A key-value pair is one key with the value it stands for, and the dictionary is the collection of its pairs.",
 "d = {'color': 'red', 'age': 42}\nprint(len(d), list(d.items())[1])", ["3 ('age', 42)", "2 ('color', 'red')", "2 42"]),
("DictionaryConstructors", "dict([('k', 1), ('k', 2)]) names the same key twice. What does the constructor do?",
 "It keeps the last value, so the dictionary has one pair with 2", ["It keeps both pairs under the one key", "It raises a KeyError for the repeated key", "It keeps the first value and ignores the second"],
 "The constructor inserts the pairs in order, and a later pair with an equal key replaces the earlier value without any error.",
 "print(dict([('k', 1), ('k', 2)]))", ["{'k': 1}", "{'k': 3}", "[('k', 2)]"]),
("KeysNotIndexes", "spam = {12345: 'Luggage Combination', 42: 'The Answer'} has two pairs. What does spam[0] ask for?",
 "A key equal to 0, which is absent, so it raises KeyError", ["The first pair that was added to the dictionary", "The value at position 0, which is 'Luggage Combination'", "A slice of the dictionary that starts at zero"],
 "The integers of a dictionary are keys chosen by the programmer, not positions, so a lookup of 0 fails when no key equals 0.",
 "spam = {12345: 'Luggage Combination', 42: 'The Answer'}\nprint(spam[0])", ["Luggage Combination", "IndexError", "None"]),
("OrderInsensitiveEquality", "When are two dictionaries equal?",
 "When they hold the same keys and the same value for each key, in any order", ["Only when their pairs were entered in the same order", "Only when they are the same object in memory", "When they have the same number of pairs"],
 "Equality of dictionaries ignores the order of the pairs, where equality of lists depends on it.",
 "print({'a': 1, 'b': 2} == {'b': 2, 'a': 1}, ['a', 'b'] == ['b', 'a'])", ["True True", "False False", "False True"]),
("InsertionOrder", "Since Python 3.7, what order does a loop over a dictionary follow?",
 "The order in which the keys were first inserted", ["The sorted order of the keys", "An arbitrary order that changes from run to run", "The order of the hash values of the keys"],
 "The language guarantees insertion order; the book's statement that a dictionary has no first item was true of older versions.",
 "d = {'one': 1, 'two': 2, 'three': 3}\nd['one'] = 42\ndel d['two']\nd['two'] = 0\nprint(list(d))", ["['one', 'two', 'three']", "['two', 'one', 'three']", "['three', 'two', 'one']"]),
("MappingNotSequence", "Why can a dictionary not be sliced like a list?",
 "It is a mapping from keys to values, and its keys are not positions", ["Because it is immutable and a slice would change it", "Because it holds too many items to copy", "Because it has no length"],
 "A sequence is reached by position; a dictionary is reached by key, so the subscript d[0:2] is looked up as a key and fails.",
 "from collections.abc import Sequence, Mapping\nprint(isinstance({}, Sequence), isinstance({}, Mapping))", ["True False", "True True", "False False"]),
("HashableKeys", "Why can a list not be used as a dictionary key?",
 "It can change, so its hash value would change and the pair would be lost", ["It is too long to be turned into a number", "It can hold only integers", "It is stored in a different part of memory"],
 "A key's hash value must stay the same for its lifetime; a list can change by an append, so it is unhashable.",
 "try:\n    d = {[1, 2]: 'x'}\nexcept TypeError:\n    print('TypeError')", ["KeyError", "ValueError", "{[1, 2]: 'x'}"]),
("HashValue", "What is the hash value of a key used for?",
 "To decide where the pair is stored and found again quickly", ["To encrypt the key so nobody can read it", "To count how many times the key was used", "To sort the keys alphabetically"],
 "Python computes a whole number from the key and uses it to jump to the place where the pair is kept, so a lookup does not scan every key.",
 "print(hash(1) == hash(1.0), hash('ab') == hash('a' + 'b'))", ["False True", "True False", "False False"]),
("TupleAsKey", "Which key can identify a point on a grid by two numbers?",
 "The tuple (2, 3), because a tuple of numbers is hashable", ["The list [2, 3], because it keeps the order", "The set {2, 3}, because it holds both numbers", "The dictionary {'x': 2, 'y': 3}, because it names them"],
 "The book's replacement for a list as a key is a tuple; a list, a set and a dictionary are unhashable.",
 "grid = {(0, 0): 'start', (2, 3): 'goal'}\nprint(grid[(2, 3)], (1, 1) in grid)", ["goal True", "start False", "None False"]),
("EqualKeysShareASlot", "Why does {1: 'a', 1.0: 'b', True: 'c'} have only one pair?",
 "The three keys compare equal and share a hash, so they are one key", ["Python drops every key that is not a string", "The values 'a', 'b' and 'c' cancel one another", "Only the first key is kept and the others raise errors"],
 "Equal keys with equal hashes name the same entry, which keeps the first key object and takes the last value.",
 "d = {1: 'a', 1.0: 'b', True: 'c'}\nprint(len(d), d[1])", ["3 a", "1 a", "3 c"]),
("KeyErrorOnMissing", "What does the text after KeyError tell you when spam['color'] fails?",
 "The key that was missing, written as Python writes it", ["The nearest key that the dictionary does hold", "The position at which the key would have been", "The value that the key had before it was deleted"],
 "The exception's single argument is the missing key, so the message names the cause directly.",
 "spam = {'name': 'Zophie', 'age': 7}\ntry:\n    print(spam['color'])\nexcept KeyError as e:\n    print(e)", ["color", "None", "KeyError"]),
("MembershipOnKeys", "What does 'red' in spam ask when spam = {'color': 'red', 'age': 42}?",
 "Whether 'red' is a key, which it is not", ["Whether 'red' is a value, which it is", "Whether 'red' is in the first pair", "Whether the dictionary is not empty"],
 "The in operator on a dictionary asks about its keys; the values have their own test, 'red' in spam.values().",
 "spam = {'color': 'red', 'age': 42}\nprint('red' in spam, 'red' in spam.values(), 'age' in spam)", ["True True True", "False False True", "True False False"]),
("GetMethod", "What does picnic_items.get('eggs', 0) do when 'eggs' is not a key?",
 "It returns 0 and leaves the dictionary unchanged", ["It raises a KeyError that names 'eggs'", "It adds the pair 'eggs': 0 and returns 0", "It returns None and prints a warning"],
 "Get returns the fallback for an absent key, without raising and without storing it.",
 "p = {'apples': 5, 'cups': 2}\nprint(p.get('eggs', 0), 'eggs' in p)", ["0 True", "None False", "2 False"]),
("SetdefaultMethod", "What does the second call spam.setdefault('color', 'white') do after 'color' was set to 'black'?",
 "It changes nothing and returns 'black'", ["It replaces the value with 'white'", "It raises a KeyError because the key exists", "It adds a second pair with the value 'white'"],
 "Setdefault stores the default only when the key is absent, and always returns the value now stored.",
 "spam = {'name': 'Pooka', 'age': 5}\nspam.setdefault('color', 'black')\nprint(spam.setdefault('color', 'white'))", ["white", "None", "color"]),
("AddOrReplacePair", "What does d['Bob'] = 'Dec 13' do when 'Bob' is already a key?",
 "It replaces the value and Bob keeps his place in the order", ["It adds a second pair for Bob at the end", "It raises a KeyError because the key exists", "It leaves the old value because keys cannot change"],
 "Assignment adds a pair for a new key and replaces the value for an existing one.",
 "d = {'Alice': 'Apr 1', 'Bob': 'Dec 12'}\nd['Eve'] = 'Dec 5'\nd['Bob'] = 'Dec 13'\nprint(len(d), d['Bob'])", ["4 Dec 13", "3 Dec 12", "2 Dec 13"]),
("DeletePair", "How does the chessboard program move the piece from e2 to e4?",
 "It copies the piece to the new key and then deletes the old key", ["It renames the key e2 to e4 in one step", "It deletes e2 first and then looks the piece up again", "It swaps the values of e2 and e4"],
 "A move is an assignment followed by a del; the order matters, because deleting first would lose the piece.",
 "b = {'e2': 'wP', 'e1': 'wK'}\nb['e4'] = b['e2']\ndel b['e2']\nprint(sorted(b))", ["['e1', 'e2']", "['e1', 'e2', 'e4']", "['e2', 'e4']"]),
("PopMethod", "What does pop('e2', None) do when 'e2' is not a key?",
 "It returns None and leaves the dictionary as it was", ["It raises a KeyError for 'e2'", "It removes the last pair instead", "It returns 'e2' unchanged"],
 "Pop removes a key and returns its value; the second argument is returned instead of an error when the key is absent.",
 "d = {'a1': 'wR', 'e2': 'wP', 'h8': 'bR'}\nprint(d.pop('e2'), d.pop('e2', None), d.popitem())", ["wP wP ('h8', 'bR')", "wP None ('a1', 'wR')", "e2 None ('h8', 'bR')"]),
("UpdateAndMerge", "In defaults | overrides, which value wins when both dictionaries have the same key?",
 "The value from the right-hand dictionary", ["The value from the left-hand dictionary", "The larger of the two values", "Neither; the key is dropped"],
 "The merge operator builds a new dictionary and the right-hand values take priority; the operands are unchanged.",
 "a = {'x': 1, 'y': 2}\nb = {'y': 20}\nprint(a | b, a)", ["{'x': 1, 'y': 2} {'x': 1, 'y': 2}", "{'x': 1, 'y': 20} {'x': 1, 'y': 20}", "{'x': 1, 'y': 22} {'x': 1, 'y': 2}"]),
("FromkeysMethod", "What is the trap in dict.fromkeys('ab', [])?",
 "Both keys share one list, so appending to one changes the other", ["The keys are made from the list, not the string", "The method raises a TypeError for a list value", "Only the first key receives the list"],
 "All the values refer to a single object; a dictionary comprehension builds a separate list for each key.",
 "d = dict.fromkeys('ab', [])\nd['a'].append(1)\nprint(d)", ["{'a': [1], 'b': []}", "{'a': [1]}", "{'a': 1, 'b': 1}"]),
("BirthdayLookup", "How does the birthdays program decide between printing a birthday and asking for one?",
 "It tests name in birthdays", ["It catches the KeyError of every lookup", "It loops over all the names until one matches", "It asks the user whether the name is known"],
 "The membership test on the keys chooses the branch; the assignment birthdays[name] = bday then adds the new pair.",
 "birthdays = {'Alice': 'Apr 1'}\nname = 'Eve'\nif name in birthdays:\n    print(birthdays[name])\nelse:\n    birthdays[name] = 'Dec 5'\n    print(len(birthdays))", ["1", "Dec 5", "KeyError"]),
("KeysValuesItems", "What does spam.items() return for spam = {'color': 'red', 'age': 42}?",
 "A view of the pairs, each as a (key, value) tuple", ["A list of the values only", "A copy of the dictionary", "A sorted list of the keys"],
 "The items view hands out the pairs, which is why a loop can unpack them into two variables.",
 "spam = {'color': 'red', 'age': 42}\nprint(list(spam.values()), len(spam.items()))", ["['color', 'age'] 2", "['red', 42] 4", "dict_values(['red', 42]) 2"]),
("LiveAndSetLikeViews", "A keys view was made before a pair was added. What does it show afterwards?",
 "The new key as well, because a view is live", ["Only the keys that existed when it was made", "Nothing, because the dictionary changed", "A KeyError for the new key"],
 "A view is a window onto the dictionary, not a copy, so it reflects later changes.",
 "d = {'a': 1}\nk = d.keys()\nd['b'] = 2\nprint(len(k), sorted(k & {'b', 'z'}))", ["1 ['b']", "2 ['b', 'z']", "2 []"]),
("ItemsLoop", "What do the variables k and v hold in for k, v in spam.items()?",
 "The key and the value of the current pair", ["The first and the last key of the dictionary", "The index and the key of the current pair", "Two copies of the same value"],
 "Each pass unpacks one (key, value) tuple into the two loop variables.",
 "total = 0\nfor k, v in {'a': 1, 'b': 2, 'c': 3}.items():\n    total = total + v\nprint(total)", ["3", "abc", "123"]),
("SortedAndReversedLoops", "How do you loop over a dictionary's pairs from the smallest value to the largest?",
 "Loop over sorted(d.items(), key=lambda kv: kv[1])", ["Loop over sorted(d) and trust the values to follow", "Loop over reversed(d)", "Loop over d.values().sort()"],
 "A loop follows insertion order; sorted with a key function that picks the value gives the order wanted.",
 "s = {'b': 2, 'a': 3, 'c': 1}\nprint(sorted(s.items(), key=lambda kv: kv[1])[0])", ["('a', 3)", "('b', 2)", "('a', 1)"]),
("ChangeWhileLooping", "What happens when a loop over a dictionary adds a new key to it?",
 "Python raises RuntimeError: the dictionary changed size during iteration", ["The loop visits the new key too and carries on", "Python raises a KeyError for the new key", "The new key is silently ignored"],
 "A loop reads the pairs by position, so a change of size is refused; loop over list(d) or build a new dictionary instead.",
 "d = {'a': 1}\ntry:\n    for k in d:\n        d[k + 'x'] = 2\nexcept RuntimeError:\n    print('RuntimeError')", ["KeyError", "{'a': 1, 'ax': 2}", "(no output)"]),
("DictComprehension", "What does the expression {v: k for k, v in d.items()} do?",
 "It builds a new dictionary with the keys and values swapped", ["It changes d in place so the values become keys", "It builds a list of the values", "It sorts the dictionary by its values"],
 "A dictionary comprehension makes a new dictionary from a loop; swapping loses a pair if two keys share a value.",
 "d = {'a': 1, 'b': 2, 'c': 3}\nprint({v: k for k, v in d.items() if v > 1})", ["{'b': 2, 'c': 3}", "{1: 'a', 2: 'b', 3: 'c'}", "{2: 'b'}"]),
("CharacterCount", "Why does characterCount.py call count.setdefault(character, 0) before adding one?",
 "So the key exists and the addition does not raise KeyError", ["So the characters are sorted before they are counted", "So each character is counted only once", "So the count starts at the length of the message"],
 "The first sight of a character has no key yet; setdefault creates it with 0 and the next line adds one.",
 "count = {}\nfor c in 'banana':\n    count.setdefault(c, 0)\n    count[c] = count[c] + 1\nprint(count)", ["{'b': 1, 'a': 1, 'n': 1}", "{'a': 3, 'b': 1, 'n': 2}", "{'b': 1, 'a': 3, 'n': 3}"]),
("CounterClass", "What does Counter('abracadabra')['z'] give?",
 "0, without adding the key z", ["A KeyError, as for a plain dictionary", "None", "The count of the nearest letter"],
 "A Counter returns 0 for an absent element and does not store it, and most_common lists the commonest first.",
 "from collections import Counter\nprint(Counter('abracadabra').most_common(2))", ["[('a', 5), ('r', 2)]", "[('a', 5), ('b', 2), ('r', 2)]", "[('b', 2), ('a', 5)]"]),
("DefaultdictCounting", "What does defaultdict(int)['y'] do when 'y' is not a key?",
 "It calls int(), stores 0 under 'y' and returns 0", ["It raises a KeyError like a plain dictionary", "It returns 0 but stores nothing", "It stores None under 'y'"],
 "A defaultdict calls its factory for a missing key on a subscript and keeps the result; get and in do not.",
 "from collections import defaultdict\nd = defaultdict(int)\nd['x'] += 1\nd['y']\nprint(dict(d))", ["{'x': 1}", "{'x': 1, 'y': None}", "KeyError"]),
("GroupingIntoLists", "What does groups.setdefault(word[0], []).append(word) do on the first word with a new letter?",
 "It creates the list for that letter and appends the word to it", ["It raises a KeyError because the letter is new", "It replaces the dictionary by a list", "It appends the word to the list of the previous letter"],
 "Setdefault returns the list stored under the key, creating it first when needed, and append adds to that same list.",
 "g = {}\nfor w in ['apple', 'avocado', 'banana']:\n    g.setdefault(w[0], []).append(w)\nprint(g)", ["{'a': ['avocado'], 'b': ['banana']}", "{'a': 'avocado', 'b': 'banana'}", "{'a': ['apple'], 'b': ['avocado', 'banana']}"]),
("MissingKeyHook", "Which operation calls __missing__ in a subclass of dict?",
 "The subscript d[key] on an absent key", ["The get method on an absent key", "The in operator on an absent key", "Every lookup, whether or not the key is present"],
 "Only d[key] reaches the hook; get and in report None and False.",
 "class Zero(dict):\n    def __missing__(self, key):\n        return 0\nz = Zero()\nprint(z['a'], 'a' in z, z.get('a'))", ["0 True 0", "KeyError", "0 False 0"]),
("DataStructureModel", "In {'h1': 'bK', 'c6': 'wQ', 'g2': 'bB', 'h5': 'bQ', 'e3': 'wK'}, what stands for an empty square?",
 "The absence of the square's key from the dictionary", ["The value None under the square's key", "The empty string under the square's key", "The value 0 under the square's key"],
 "The model remembers only the pieces; the squares that are not mentioned are empty.",
 "board = {'h1': 'bK', 'c6': 'wQ', 'g2': 'bB', 'h5': 'bQ', 'e3': 'wK'}\nprint(len(board), board['c6'], 'a1' in board)", ["64 wQ False", "5 wQ True", "5 c6 False"]),
("ChessboardModel", "Why does the program reset the board with copy.copy(STARTING_PIECES)?",
 "So changes to the working board do not change the constant", ["Because a dictionary cannot be assigned twice", "Because the pieces must be sorted first", "Because copy.copy checks that the position is legal"],
 "The constant holds the 32-piece starting position; a copy gives the program a board to change.",
 "S = {c + '2': 'wP' for c in 'abcdefgh'}\nS['e4'] = S.pop('e2')\nprint(len(S), 'e2' in S, S['e4'])", ["9 False wP", "8 True wP", "7 False wP"]),
("BoardTemplate", "What fills the 64 pairs of curly brackets in BOARD_TEMPLATE?",
 "The strings of the squares, put in by the format method in order", ["The keys of the chessboard dictionary, sorted", "The numbers 1 to 64", "Nothing; they draw the frame of the board"],
 "The template separates the look of the board from the logic; format replaces the first {} with its first argument and so on.",
 "print('| {} | {} |'.format('wK', 'bK'))", ["| {} | {} |", "| wK | wK |", "| bK | wK |"]),
("ChessboardPrinter", "How does print_chessboard decide what to put on a square?",
 "It asks whether x + y is a key of the board", ["It searches the board's values for the square name", "It counts the pieces on the board first", "It reads the square from the template"],
 "A key means a piece stands there, and no key means an empty square, so one membership test decides.",
 "board = {'h1': 'bK'}\nn = 0\nfor y in '87654321':\n    for x in 'abcdefgh':\n        if x + y in board:\n            n = n + 1\nprint(n)", ["64", "8", "0"]),
("StarSyntax", "What does print(*spam) do for spam = ['cat', 'dog', 'rat']?",
 "It passes the items as separate arguments and prints cat dog rat", ["It prints the list with brackets and quotes", "It multiplies the list by itself", "It prints only the first item"],
 "A star before a list in a call unpacks it; it is why format(*squares) receives 64 arguments.",
 "spam = ['cat', 'dog', 'rat']\nprint(*spam)", ["['cat', 'dog', 'rat']", "cat, dog, rat", "catdograt"]),
("ChessboardCommands", "What does input('> ').split() give for the line move e2 e4?",
 "The list ['move', 'e2', 'e4']", ["The string 'move e2 e4' unchanged", "The tuple ('move', 'e2e4')", "The dictionary {'move': 'e2'}"],
 "Split cuts the line into words, and the first word chooses the command.",
 "response = 'move e2 e4'.split()\nprint(response[0], len(response))", ["move 2", "e2 3", "move e2"]),
("NestedDictionaries", "What does all_guests['Bob']['apples'] do?",
 "It looks up Bob's dictionary and then the apples in it", ["It looks up the key 'Bob apples'", "It returns a list of Bob and apples", "It adds the two keys together"],
 "A chained lookup moves one level for each pair of brackets.",
 "g = {'Alice': {'apples': 5}, 'Bob': {'apples': 2, 'cups': 1}}\nprint(g['Bob']['apples'], g['Alice'].get('cups', 0))", ["5 0", "2 1", "2 KeyError"]),
("TotalBrought", "Why does total_brought use v.get(item, 0) and not v[item]?",
 "A guest who brings none of the item must add zero and not raise KeyError", ["Because v[item] would change the dictionary", "Because get sorts the guests", "Because v[item] is slower than get"],
 "The inner dictionaries do not share their keys, so the fallback keeps the loop running.",
 "guests = {'Alice': {'apples': 5}, 'Bob': {'apples': 2, 'cups': 1}}\ntotal = 0\nfor k, v in guests.items():\n    total = total + v.get('apples', 0)\nprint(total)", ["2", "5", "8"]),
("CopyingDictionaries", "What does copy.copy of a nested dictionary share with the original?",
 "The inner dictionaries, which are the same objects", ["Nothing; every level is copied", "Only the keys", "The outer dictionary, as a second name"],
 "A shallow copy makes a new outer dictionary; copy.deepcopy copies every level.",
 "import copy\no = {'A': {'n': 5}}\ns = copy.copy(o)\nd = copy.deepcopy(o)\no['A']['n'] = 99\nprint(s['A']['n'], d['A']['n'])", ["5 5", "99 99", "5 99"]),
("PrettyPrinting", "Which module and function pretty-print a dictionary?",
 "The pprint module and its pprint function", ["The print module and its pretty function", "The json module and its pretty function", "The copy module and its pprint function"],
 "The pprint module prints nested data in a readable layout, with the keys sorted by default.",
 "import pprint\nprint(pprint.pformat({'b': 1, 'a': 2}))", ["{'b': 1, 'a': 2}", "{'a': 1, 'b': 2}", "[('a', 2), ('b', 1)]"]),
("JsonText", "What happens to the key 1 of {1: 'a'} when it goes through json.dumps and json.loads?",
 "It comes back as the string '1', because JSON keys are strings", ["It comes back unchanged as the integer 1", "It is dropped, because JSON keys must be letters", "It raises a TypeError"],
 "JSON objects have string keys, so the round trip is not exact; tuples come back as lists.",
 "import json\nprint(json.dumps({'ok': True, 'n': None}))", ["{'ok': True, 'n': None}", "{\"ok\": True, \"n\": None}", "{\"ok\": true, \"n\": \"null\"}"]),
("TypedModels", "What does Python check at run time about a TypedDict?",
 "Nothing; it creates an ordinary dict and a type checker does the checking", ["That every key is present", "That each value has the declared type", "That no other key is added"],
 "A TypedDict class declares the shape for static tools; at run time the object is a plain dictionary.",
 "from typing import TypedDict\nclass Cat(TypedDict):\n    size: str\n    age: int\nc = Cat(size='fat', age='old')\nprint(type(c).__name__, c['age'])", ["Cat old", "TypeError", "dict 17"]),
("MappingPattern", "Does the pattern {'type': 'move', 'from': a, 'to': b} match a dictionary that has an extra key?",
 "Yes; extra keys are ignored and a and b are bound", ["No; the keys must be exactly those three", "Yes, but a and b stay unbound", "No; a mapping pattern needs a defaultdict"],
 "A mapping pattern matches when its keys are present and their value patterns match.",
 "cmd = {'type': 'move', 'from': 'e2', 'to': 'e4', 'extra': 1}\nmatch cmd:\n    case {'type': 'move', 'from': a, 'to': b}:\n        print(a, b)\n    case _:\n        print('unknown')", ["unknown", "move e2", "e2 e4 1"]),
("PracticeQuestions", "What is the shortcut for: if 'color' not in spam: spam['color'] = 'black'?",
 "spam.setdefault('color', 'black')", ["spam.get('color', 'black')", "spam['color'] or 'black'", "spam.update('color', 'black')"],
 "Setdefault stores the default only when the key is absent, in one line.",
 "spam = {}\nspam.setdefault('color', 'black')\nprint(spam, 'cat' in {'cat': 1}.values())", ["{} False", "{'color': 'black'} True", "{'color': None} False"]),
("ChessValidator", "Which check belongs in a chessboard validator?",
 "Exactly one king of each colour and every key a square from a1 to h8", ["That the pieces stand on squares of the same colour", "That white has more pieces than black", "That every piece has moved at least once"],
 "The validator counts the pieces with a dictionary and tests the shape of every key and value.",
 "board = {'e3': 'wK', 'e1': 'wK', 'h1': 'bK'}\ncount = {}\nfor piece in board.values():\n    count[piece] = count.get(piece, 0) + 1\nprint(count['wK'])", ["1", "3", "KeyError"]),
("FantasyInventory", "In display_inventory, what do k and v hold in for k, v in inventory.items()?",
 "k is the item name and v is how many the player has", ["k is how many and v is the item name", "k is the position and v is the pair", "Both hold the item name"],
 "The keys name the items and the values count them, so the total is the sum of the values.",
 "stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}\nprint(sum(stuff.values()), len(stuff))", ["5 62", "62 62", "61 5"]),
("LootConversion", "How does add_to_inventory count the items of a list that repeats an item?",
 "It makes sure the key exists with setdefault and adds one for each occurrence", ["It replaces the count with the number of items in the list", "It adds the list as a value under each key", "It sorts the list and counts the distinct items"],
 "It is the character count of this chapter again, with items in place of characters.",
 "inv = {'gold coin': 42, 'rope': 1}\nfor item in ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']:\n    inv.setdefault(item, 0)\n    inv[item] = inv[item] + 1\nprint(sum(inv.values()), inv['gold coin'])", ["47 45", "48 43", "5 3"]),
]
# (concept, question, right, [3 wrong], why) for every branch and section
UPPER = [
("DictionaryModel", "What is the dictionary data type for?", "Finding each of many values by a key of its own", ["Keeping values in a fixed numbered order", "Doing arithmetic on many numbers at once", "Reading lines from a file"], "A dictionary joins keys to values, so data about one thing lives in one variable under names that explain themselves."),
("PairsAndMappings", "Which words name the parts of a dictionary and the kind of object it is?", "Key-value pairs, and a mapping", ["Index-item pairs, and a sequence", "Rows and columns, and a table", "Names and types, and a class"], "A dictionary is a collection of key-value pairs and Python calls an object that joins keys to values a mapping."),
("ListContrast", "Which of these is true of a dictionary but not of a list?", "Two dictionaries with the same pairs are equal in any order", ["It can be changed after it is created", "It can hold other lists and dictionaries", "It can be looped over with for"], "The chapter's contrasts are keys instead of indexes, equality that ignores order, and no slicing."),
("KeyRules", "What is the rule for a dictionary key?", "It must be hashable", ["It must be a string", "It must be a whole number", "It must be shorter than 10 characters"], "Hashable values such as strings, numbers and tuples of them may be keys; lists and dictionaries may not."),
("WhatMayBeAKey", "Which of these may be a dictionary key?", "A tuple of numbers", ["A list of numbers", "A set of numbers", "A dictionary of numbers"], "A key needs a hash value that never changes, which a tuple of numbers has and a mutable container does not."),
("AbsentKeys", "What does Python raise when a lookup asks for a key that is not there?", "KeyError", ["IndexError", "ValueError", "NameError"], "KeyError is to a dictionary what IndexError is to a list."),
("ReadingAndChanging", "Which operations does the branch on reading and changing pairs cover?", "Looking up safely, adding, replacing, removing and combining pairs", ["Sorting, searching and printing a table", "Opening, reading and writing files", "Importing modules and defining functions"], "Almost every program that uses a dictionary does these few things."),
("Reading", "Which three tools read a pair without risking a KeyError?", "The in test, get and setdefault", ["The del statement, pop and update", "keys, values and items", "sorted, reversed and len"], "Each answers a different need: branching on presence, wanting a value or a default, and wanting a key that must exist afterwards."),
("Changing", "Which statement changes a dictionary by removing a pair?", "del d[key]", ["d.get(key)", "d.keys()", "key in d"], "A dictionary is mutable: assignment adds or replaces a pair, del and pop remove one."),
("FirstProgram", "What does the birthdays program show about a dictionary?", "It can be a lookup table that changes while the program runs", ["It can be saved to disk automatically", "It can sort its names alphabetically", "It cannot be changed after it is created"], "The program tests, reads and adds pairs, and forgets everything when it ends."),
("ViewsAndLoops", "What is the branch on views and loops about?", "Going through a dictionary by its keys, values or pairs", ["Printing a dictionary to a file", "Converting a dictionary to JSON", "Choosing hashable keys"], "The three views feed for loops, sorted and reversed, and the comprehension builds a new dictionary from a loop."),
("Views", "What is a dictionary view?", "A live window onto the dictionary's keys, values or pairs, not a copy", ["A copy of the dictionary made at one moment", "A sorted list of its keys", "A read-only dictionary of the same pairs"], "The views are dynamic: when the dictionary changes, the view reflects the changes."),
("Looping", "In which order does a for loop over a dictionary visit its keys?", "In the order in which they were inserted", ["In alphabetical order", "In the order of their hash values", "In a random order each run"], "Since Python 3.7 a dictionary keeps insertion order."),
("Building", "What does a dictionary comprehension build?", "A new dictionary from a loop, in one expression", ["A list of the dictionary's keys", "A copy that shares the old values", "A set of the pairs"], "The form is {key: value for item in iterable}, with an optional if."),
("CountingAndGrouping", "Which two jobs are dictionaries most often used for in practice?", "Counting things and grouping them under labels", ["Sorting things and deleting them", "Reading files and writing files", "Adding numbers and subtracting them"], "Both jobs start with a key that does not yet exist, and the branch shows three ways of coping."),
("Counting", "Which tools count items with a dictionary in the standard library or the book?", "The setdefault pattern, Counter and defaultdict", ["The sorted, reversed and len functions", "The copy, deepcopy and pprint functions", "The json, csv and re modules"], "Each makes sure a count exists before one is added."),
("Grouping", "What does a dictionary of lists do?", "Collects the items that share a label in one list under that label", ["Counts how many items have each label", "Sorts the items by their labels", "Removes the duplicates of each label"], "The value is a collection and the main step is putting each item into the collection of its key."),
("StructuringData", "What does the branch on structuring data teach?", "Designing the dictionary that models a thing, and displaying, copying and writing it down", ["Writing a chess-playing program", "Installing a graphics library", "Reading the rules of chess"], "The chapter's claim is that real-world objects and processes can be modelled by data structures and functions that work with them."),
("Modelling", "What does the chessboard simulator model?", "The position of the pieces, as a dictionary from squares to pieces", ["The rules by which each piece moves", "The strength of each side", "The history of the moves played"], "The program does not enforce the rules of chess; it holds a position and does what the user says."),
("Nesting", "What are nested structures?", "Dictionaries and lists that contain other dictionaries and lists", ["Dictionaries that cannot be changed", "Loops that contain other loops", "Functions defined inside functions"], "The picnic example is a dictionary of guests in which every guest has a dictionary of items."),
("Notation", "Which of these is a way of writing a data structure down as text?", "JSON, through the json module", ["The del statement", "The match statement without patterns", "The star before a list in a call"], "Pretty-printing, JSON, TypedDict and the mapping pattern each answer a need to look at, save, describe or take apart a structure."),
("PracticeWork", "What do the practice questions and programs of the chapter test?", "Whether the chapter's operations can be used on a new problem", ["Whether the reader can type quickly", "Whether the reader knows the rules of chess", "Whether the reader can install packages"], "The three programs check a structure, display it and build it from a list."),
("ReviewQuestions", "How many practice questions end the chapter, and what do they ask?", "Eight, on the vocabulary and operations of dictionaries", ["Three, on the chessboard", "Twelve, on the hash function", "One, on JSON"], "Each answer points back to one concept of the chapter."),
("PracticePrograms", "Which three programs are the practice programs?", "A chess dictionary validator, a fantasy game inventory and a loot conversion", ["A calculator, a clock and a notebook", "A chat client, a web server and a database", "A sorter, a searcher and a counter"], "They apply the chapter to checking, displaying and building a dictionary."),
]


SUFFIXES = [" every time the line runs", ", whatever keys the dictionary holds", " in every version of Python", ", as the program is written", " each time it is called"]


def run(code):
    r = subprocess.run([sys.executable if False else "/root/.local/bin/python3.14", "-c", code], capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
    if r.returncode == 0:
        return r.stdout.strip() or "(no output)"
    lines = [l for l in r.stderr.strip().splitlines() if l.strip()]
    return lines[-1].split(":")[0].strip()


def build():
    ids = [n[0] for n in C.NODES]; label = {n[0]: n[1] for n in C.NODES}
    items = []
    seq = []
    for cid, q, right, wrong, why, code, awrong in LEAF:
        seq.append(("U", cid, q, right, wrong, why, None))
        out = run(code)
        assert out not in awrong, (cid, out, awrong)
        seq.append(("A", cid, label[cid] + ": what does this program print?", out, awrong, "Run under Python 3.14: " + out.replace("\n", " ") + ". " + why, code))
    for cid, q, right, wrong, why in UPPER:
        seq.append(("U", cid, q, right, wrong, why, None))
    # order: by concept order of the corpus, Understand before Apply
    order = {c: i for i, c in enumerate(ids)}
    seq.sort(key=lambda s: (order[s[1]], s[0] == "A"))
    for k, (kind, cid, q, right, wrong, why, code) in enumerate(seq):
        pos = k % 4
        wrong = list(wrong)
        if kind == "U" and k % 3 != 0 and len(right) >= max(len(w) for w in wrong):
            # the right answer must not be recognisable by its length: lengthen the longest wrong option with neutral wording
            j = max(range(len(wrong)), key=lambda t: len(wrong[t]))
            for suffix in SUFFIXES:
                if len(wrong[j]) > len(right):
                    break
                wrong[j] = wrong[j] + suffix
        opts = list(wrong); opts.insert(pos, right)
        it = {"concept": cid, "level": "Apply" if kind == "A" else "Understand", "q": q}
        if code: it["code"] = code
        it.update({"options": opts, "answer": pos, "why": why})
        items.append(it)
    missing = set(ids) - {i["concept"] for i in items}
    assert not missing, missing
    return items


if __name__ == "__main__":
    items = build()
    json.dump(items, open(os.path.join(HERE, "question_bank_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
    print(len(items), "items;", sum(1 for i in items if i["level"] == "Apply"), "Apply with code;", len({i["concept"] for i in items}), "concepts")
