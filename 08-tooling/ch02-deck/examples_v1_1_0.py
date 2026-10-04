__version__ = "1.1.0"
# Every code example the renewed chapter 2 lecture deck shows. Nothing here carries an output: the outputs are produced
# by executing each line and each program under the course interpreter at build time (ch01-deck/examples_run_v2_1_0.py),
# so a slide can only show what Python actually printed.
#
# EX holds interactive-shell sessions, each run in a namespace of its own, line by line, exactly the way
# ch02-deck/deck_check_v1_0_1.py re-runs them from the finished slides. A statement records no output and must be
# followed by another line in the same card; no line may print, because printing examples belong in PROGRAMS.
# PROGRAMS holds whole programs; a third element "mayfail" marks a program that is meant to stop with an error, which
# is how the chapter teaches the unassigned name and the input guard.
#
# 1.1.0 keeps the sessions of 1.0.1 and adds one session or one program for each of the 53 leaf concepts of the chapter
# corpus (sen0414_ch02_corpus_v1_0_0.py) that has a worked example. Additive, so MINOR.
EX = {
 # --- group cards: one short session to open each group of concepts ---
 "truthgroup":["True", "bool(1)", "bool(0)", "bool('text')"],
 "eqgroup":   ["'hello' == 'hello'", "42 == '42'", "None is None"],
 "ordgroup":  ["5 <= 5", "1 < 2 < 3", "'apple' < 'banana'"],
 "logicgroup":["(4 < 5) and (5 < 6)", "False or True", "not not not not True"],
 "stmtexpr":  ["spam = 42", "spam", "2 + 2"],
 # --- I. Values: the Boolean, truthiness, None, and the collections ---
 "boolean":   ["42 == 42", "42 == 99", "True + True", "int(True)", "'True' == True"],
 "truthiness":["bool('')", "bool(' ')", "bool('0')", "bool(0.0)", "bool([0])", "[] == False"],
 "none":      ["bool(None)", "None == False", "None == 0", "None or 'default'", "type(None)"],
 "container": ["len([10, 20, 30])", "len('')", "type({})", "bool([[]])", "bool([])"],
 # --- II. Comparison ---
 "equality":  ["42 == 42.0", "42 == '42'", "'hello' == 'Hello'", "0.1 + 0.2 == 0.3", "2 != 3"],
 "eqassign":  ["4 == 2 + 2", "spam = 4", "spam == 4", "spam"],
 "identity":  ["None is None", "x = None", "x is None", "x is not None"],
 "ordering":  ["42 < 100", "42 < 42", "42 <= 42", "1.999 < 5", "3 < '4'"],
 "chained":   ["1 < 2 < 3", "3 > 2 > 5", "5 < 3 < 1 / 0", "1 < 2 > 1.5"],
 "strorder":  ["'apple' < 'banana'", "ord('a')", "ord('Z')", "'Z' < 'a'", "'10' < '9'"],
 # --- III. Boolean operations ---
 "andop":     ["True and True", "True and False", "False and True", "False and False", "(4 < 5) and (9 < 6)"],
 "orop":      ["False or True", "False or False", "(1 == 2) or (2 == 2)", "'GB' == 'TB' or 'tb'"],
 "notop":     ["not True", "not False", "not 'foo'", "not ''", "not 4 == 5"],
 "arity":     ["5 - 3", "-(2 + 3)", "4 - -2", "4 - (-2)"],
 "shortcirc": ["1 or 1 / 0", "0 and 1 / 0", "False and 1 / 0", "1 and 1 / 0"],
 "operand":   ["'hi' and 'there'", "'' and 'there'", "'' or 'default'", "1 and 2 and 3", "0 or [] or None"],
 "boolexpr":  ["2 + 2 == 4", "(4 < 5) and (5 < 6)", "(1 == 2) or (2 == 2)"],
 "boolprec":  ["True or False and False", "(True or False) and False", "not True and False", "not (True and False)"],
 # --- IV. Flow control ---
 "condition": ["3000 > 100", "bool('Alice')", "True == True", "bool('')"],
 "keyword":   ["__import__('keyword').iskeyword('if')", "__import__('keyword').iskeyword('true')",
               "__import__('keyword').iskeyword('match')", "__import__('keyword').issoftkeyword('match')"],
 "colonless": ["if True", "if = 3", "False = 2 + 2"],
 "condexpr":  ["'even' if 10 % 2 == 0 else 'odd'", "'even' if 7 % 2 == 0 else 'odd'", "'adult' if 20 >= 18 else 1 / 0"],
 "walrus":    ["(limit := 10) > 5", "limit", "x := 3"],
 # --- V. Modern practice: style ---
 "stylebool": ["'hello' == True", "bool('hello')", "True == True", "False == True"],
 "singleton": ["None is None", "None == False", "None == 0"],
 "emptiness": ["bool([])", "len([])", "bool([1, 2])", "len([1, 2])"],
 # --- VI. Decision patterns ---
 "toggle":    ["flag = True", "flag = not flag", "flag", "not False"],
 "insens":    ["'tb' == 'TB' or 'tb' == 'tb'", "'Tb' == 'TB' or 'Tb' == 'tb'", "'GB' == 'TB' or 'tb'"],
 # --- VII. Error reports ---
 "nameerr":   ["true", "4 + spam * 3", "discrepancy"],
 "typeerr":   ["3 < '4'", "'Alice' + 42", "42 == '42'"],
 "zerodiv":   ["1 / 0", "1 % 0", "1 / 0.0"],
 "syntaxerr": ["if = 3", "4 == not 5", "x := 3"],
}

PROGRAMS = {
 # --- flow of execution, blocks and indentation ---
 "finger_v1_0_0.py": ("age = 70\nif age > 65:\n    print('senior')\nprint('end')\n", [[]]),
 "password_v1_0_0.py": (
  "username = 'Mary'\n"
  "password = 'swordfish'\n"
  "if username == 'Mary':\n"
  "    print('Hello, Mary')\n"
  "    if password == 'swordfish':\n"
  "        print('Access granted.')\n"
  "    else:\n"
  "        print('Wrong password.')\n", [[]]),
 "indent_in_v1_0_0.py": ("x = 1\nif x > 3:\n    print('big')\n    print('always')\nprint('end')\n", [[]]),
 "indent_out_v1_0_0.py": ("x = 1\nif x > 3:\n    print('big')\nprint('always')\nprint('end')\n", [[]]),
 "skipped_v1_0_0.py": ("if False:\n    print(1 + 'a')\nprint('done')\n", [[]]),
 # --- branching ---
 "alice_v1_0_0.py": ("name = 'Bob'\nif name == 'Alice':\n    print('Hi, Alice.')\nelse:\n    print('Hello, stranger.')\n", [[]]),
 "vampire_v1_0_0.py": (
  "name = 'Carol'\n"
  "age = 3000\n"
  "if name == 'Alice':\n"
  "    print('Hi, Alice.')\n"
  "elif age < 12:\n"
  "    print('You are not Alice, kiddo.')\n"
  "elif age > 2000:\n"
  "    print('Unlike you, Alice is not an undead, immortal vampire.')\n"
  "elif age > 100:\n"
  "    print('You are not Alice, grannie.')\n", [[]]),
 "vampire_reordered_v1_0_0.py": (
  "name = 'Carol'\n"
  "age = 3000\n"
  "if name == 'Alice':\n"
  "    print('Hi, Alice.')\n"
  "elif age < 12:\n"
  "    print('You are not Alice, kiddo.')\n"
  "elif age > 100:\n"
  "    print('You are not Alice, grannie.')\n"
  "elif age > 2000:\n"
  "    print('Unlike you, Alice is not an undead, immortal vampire.')\n", [[]]),
 "littlekid_v1_0_0.py": (
  "name = 'Carol'\n"
  "age = 3000\n"
  "if name == 'Alice':\n"
  "    print('Hi, Alice.')\n"
  "elif age < 12:\n"
  "    print('You are not Alice, kiddo.')\n"
  "else:\n"
  "    print('You are neither Alice nor a little kid.')\n", [[]]),
 "chain_vs_separate_v1_0_0.py": (
  "age = 70\n"
  "if age > 12:\n"
  "    print('A')\n"
  "if age > 65:\n"
  "    print('B')\n"
  "print('--- now the same tests as one chain ---')\n"
  "if age > 12:\n"
  "    print('A')\n"
  "elif age > 65:\n"
  "    print('B')\n", [[]]),
 # --- expression forms ---
 "walrus_size_v1_0_0.py": ("name = 'Alice'\nif (size := len(name)) > 3:\n    print(size)\n", [[]]),
 # --- pattern matching ---
 "match_command_v1_0_0.py": (
  "command = 'quit'\n"
  "match command:\n"
  "    case 'go':\n"
  "        print('going')\n"
  "    case 'quit':\n"
  "        print('bye')\n"
  "    case _:\n"
  "        print('unknown')\n", [[]]),
 "match_status_v1_0_0.py": (
  "status = 403\n"
  "match status:\n"
  "    case 400:\n"
  "        print('bad request')\n"
  "    case 401 | 403 | 404:\n"
  "        print('not allowed')\n"
  "    case _:\n"
  "        print('other')\n", [[]]),
 "match_capture_v1_0_0.py": (
  "expected = 'quit'\n"
  "command = 'go'\n"
  "match command:\n"
  "    case expected:\n"
  "        print('matched', expected)\n", [[]]),
 "match_nomatch_v1_0_0.py": (
  "command = 'dance'\n"
  "match command:\n"
  "    case 'go':\n"
  "        print('going')\n"
  "print('after')\n", [[]]),
 "match_sequence_v1_0_0.py": (
  "command = ['go', 'north']\n"
  "match command:\n"
  "    case ['go', direction]:\n"
  "        print('going ' + direction)\n"
  "    case ['quit']:\n"
  "        print('bye')\n"
  "    case _:\n"
  "        print('unknown')\n", [[]]),
 "match_guard_v1_0_0.py": (
  "for point in [(3, 3), (3, 4)]:\n"
  "    match point:\n"
  "        case (x, y) if x == y:\n"
  "            print('on the diagonal at', x)\n"
  "        case (x, y):\n"
  "            print('elsewhere')\n", [[]]),
 "softkeyword_v1_0_0.py": ("match = 3\ncase = 4\nprint(match + case)\n", [[]]),
 # --- style ---
 "stylebool_v1_0_0.py": (
  "greeting = 'hello'\n"
  "if greeting == True:\n"
  "    print('equal to True')\n"
  "if greeting:\n"
  "    print('counts as true')\n", [[]]),
 "singleton_v1_0_0.py": ("x = []\nprint(x is not None, bool(x))\n", [[]]),
 "identity_v1_0_0.py": ("a = [1, 2]\nb = [1, 2]\nc = a\nprint(a == b, a is b, a is c)\n", [[]]),
 "shortcircuit_v1_0_0.py": (
  "x = 0\n"
  "print(x != 0 and 10 / x > 2)\n"
  "False and print('this is never printed')\n"
  "True and print('this is printed')\n", [[]]),
 # --- the worked programs of the chapter ---
 "oppositeday_v1_0_0.py": (
  "today_is_opposite_day = True\n"
  "if today_is_opposite_day == True:\n"
  "    say_it_is_opposite_day = True\n"
  "else:\n"
  "    say_it_is_opposite_day = False\n"
  "if today_is_opposite_day == True:\n"
  "    say_it_is_opposite_day = not say_it_is_opposite_day\n"
  "if say_it_is_opposite_day == True:\n"
  "    print('Today is Opposite Day.')\n"
  "else:\n"
  "    print('Today is not Opposite Day.')\n", [[]]),
 "capacity_v1_0_0.py": (
  "advertised = 10\n"
  "unit = 'TB'\n"
  "if unit == 'TB' or unit == 'tb':\n"
  "    discrepancy = 1000000000000 / 1099511627776\n"
  "elif unit == 'GB' or unit == 'gb':\n"
  "    discrepancy = 1000000000 / 1073741824\n"
  "real_capacity = advertised * discrepancy\n"
  "print('Real capacity: ' + str(round(real_capacity, 2)) + ' ' + unit)\n", [[]]),
 # a program that is meant to stop: the variable is assigned only inside the two branches
 "capacity_bug_v1_0_0.py": (
  "advertised = 10\n"
  "unit = 'KB'\n"
  "if unit == 'TB' or unit == 'tb':\n"
  "    discrepancy = 1000000000000 / 1099511627776\n"
  "elif unit == 'GB' or unit == 'gb':\n"
  "    discrepancy = 1000000000 / 1073741824\n"
  "real_capacity = advertised * discrepancy\n"
  "print(real_capacity)\n", [[]], "mayfail"),
 # a program that is correct in its text but fails when the faulty line is reached
 "runtime_error_v1_0_0.py": ("print('start')\nprint(1 + 'a')\nprint('never reached')\n", [[]], "mayfail"),
 # and the same capacity program with the guard the book recommends
 "capacity_guard_v1_0_0.py": (
  "import sys\n"
  "advertised = 10\n"
  "unit = 'KB'\n"
  "if unit == 'TB' or unit == 'tb':\n"
  "    discrepancy = 1000000000000 / 1099511627776\n"
  "elif unit == 'GB' or unit == 'gb':\n"
  "    discrepancy = 1000000000 / 1073741824\n"
  "else:\n"
  "    sys.exit('You must enter TB or GB')\n"
  "print(advertised * discrepancy)\n", [[]], "mayfail"),
}
