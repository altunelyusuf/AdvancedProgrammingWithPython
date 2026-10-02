#!/usr/bin/env python3
"""SEN0414 chapter 3 corpus, version 1.0.0: the concepts of the chapter, each explained in four to six paragraphs of connected prose
that answer what it is, why it matters, where it is met, how it works and what to watch for.

Used by sen0414_chapter_build_v1_0_0.py (TBox/ABox: the leaf individuals; document: one section per concept, paragraphs joined by a
blank line and printed without the question each answers). Every quoted claim was taken from text actually read on 2026-10-01
(chapter 3 of the 3rd edition at automatetheboringstuff.com; docs.python.org tutorial, language reference, library reference,
glossary and What's New 3.14; PEPs 8, 572, 618 and 765) and every number, output, error message or warning was executed (CHECKS and
RAISES below, run by this file's __main__ under any interpreter given on the command line).
"""
__version__ = "1.0.0"
W, Y, E, H, K, C = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out", "What changed"
# Citation markers are expanded to author-year strings after NODES is built (see the end of the file); each string must resolve in the
# research record sen0414_ch03_research_v1_1_0.ttl, which is checked by __main__.
CITES = {"[[SW]]": "(Sweigart, 2025)", "[[PSF]]": "(Python Software Foundation, 2026)", "[[PEP8]]": "(van Rossum, Warsaw and Coghlan, 2001)",
         "[[P572]]": "(Angelico, Peters and van Rossum, 2018)", "[[P618]]": "(Bucher, 2020)", "[[P765]]": "(Katriel and Coghlan, 2024)"}

# Programs executed by CHECKS (name -> source). Every one is run by the checker under the interpreter given on the command line.
PG = {
 "if": "spam = 0\nif spam < 5:\n    print('Hello, world.')\n    spam = spam + 1\n",
 "while": "spam = 0\nwhile spam < 5:\n    print('Hello, world.')\n    spam = spam + 1\n",
 "while_count": "spam = 0\npasses = 0\nwhile spam < 5:\n    passes = passes + 1\n    spam = spam + 1\nprint(passes)\n",
 "while_false": "while False:\n    print('never')\nprint('done')\n",
 "while_stuck": "spam = 0\nwhile spam < 5:\n    pass\n",
 "while_true_stuck": "while True:\n    pass\n",
 "yourname": "name = ''\nwhile name != 'your name':\n    print('Please type your name.')\n    name = input('>')\nprint('Thank you!')\n",
 "yourname2": "while True:\n    print('Please type your name.')\n    name = input('>')\n    if name == 'your name':\n        break\nprint('Thank you!')\n",
 "break3": "n = 0\nwhile True:\n    n = n + 1\n    if n == 3:\n        break\nprint(n)\n",
 "swordfish": "while True:\n    print('Who are you?')\n    name = input('>')\n    if name != 'Joe':\n        continue\n    print('Hello, Joe. What is the password? (It is a fish.)')\n    password = input('>')\n    if password == 'swordfish':\n        break\nprint('Access granted.')\n",
 "five_for": "print('Hello!')\nfor i in range(5):\n    print('On this iteration, i is set to ' + str(i))\nprint('Goodbye!')\n",
 "five_while": "print('Hello!')\ni = 0\nwhile i < 5:\n    print('On this iteration, i is set to ' + str(i))\n    i = i + 1\nprint('Goodbye!')\n",
 "while_continue_stuck": "i = 0\nwhile i < 5:\n    if i == 2:\n        continue\n    i = i + 1\n",
 "for_continue": "for i in range(5):\n    if i == 2:\n        continue\nprint(i)\n",
 "gauss": "total = 0\nfor num in range(101):\n    total = total + num\nprint(total)\n",
 "gauss_reset": "for num in range(101):\n    total = 0\n    total = total + num\nprint(total)\n",
 "gauss_noinit": "for num in range(101):\n    total = total + num\n",
 "last_i": "for i in range(5):\n    pass\nprint(i)\n",
 "nested_count": "n = 0\nfor i in range(4):\n    for j in range(3):\n        n = n + 1\nprint(n)\n",
 "nested_break": "for i in range(2):\n    for j in range(3):\n        if j == 1:\n            break\n        print(i, j)\n",
 "primes": "for n in range(2, 10):\n    for x in range(2, n):\n        if n % x == 0:\n            print(n, 'equals', x, '*', n//x)\n            break\n    else:\n        print(n, 'is a prime number')\n",
 "forelse_empty": "for x in []:\n    pass\nelse:\n    print('else')\n",
 "whileelse": "n = 3\nwhile n > 0:\n    n = n - 1\nelse:\n    print('else ran', n)\n",
 "break_else": "for x in [1, 2, 3]:\n    if x == 2:\n        break\nelse:\n    print('no break')\nprint('after')\n",
 "iscope": "for i in range(3):\n    pass\nprint(i)\n",
 "jscope": "for j in []:\n    pass\nprint(j)\n",
 "overwrite": "for i in range(10):\n    print(i)\n    i = 5\n",
 "break_value": "for i in range(10):\n    if i == 3:\n        break\nprint(i)\n",
 "exit0": "import sys\nsys.exit()\n",
 "exit3": "import sys\nsys.exit(3)\n",
 "exitmsg": "import sys\nsys.exit('bad')\n",
 "exitfinally": "import sys\ntry:\n    sys.exit()\nfinally:\n    print('cleanup')\n",
 "exitcatch": "import sys\ntry:\n    sys.exit(3)\nexcept SystemExit as ex:\n    print('caught', ex.code)\nprint('still running')\n",
 "exitexample": "import sys\nwhile True:\n    print('Type exit to exit.')\n    response = input('>')\n    if response == 'exit':\n        sys.exit()\n    print('You typed ' + response + '.')\n",
 "kbint": "try:\n    while True:\n        raise KeyboardInterrupt\nexcept KeyboardInterrupt:\n    print('stopped')\n",
 "kbint_loose": "while True:\n    raise KeyboardInterrupt\n",
 "finally_break": "for i in range(2):\n    try:\n        raise ValueError\n    finally:\n        break\nprint('done')\n",
 "finally_order": "for i in range(3):\n    try:\n        if i == 1:\n            break\n    finally:\n        print('cleanup', i)\n",
 "handle": "try:\n    int('x')\nexcept ValueError:\n    print('bad number')\n",
 "mutate_dict": "users = {'Ada': 'active', 'Can': 'inactive'}\nfor u in users:\n    del users[u]\n",
 "mutate_dict_copy": "users = {'Ada': 'active', 'Can': 'inactive', 'Eda': 'inactive'}\nfor name, status in users.copy().items():\n    if status == 'inactive':\n        del users[name]\nprint(users)\n",
 "mutate_list": "a = [1, 2, 2, 3]\nfor x in a:\n    if x == 2:\n        a.remove(x)\nprint(a)\n",
 "mutate_list_new": "a = [1, 2, 2, 3]\nb = []\nfor x in a:\n    if x != 2:\n        b.append(x)\nprint(b)\n",
 "break_cond": "n = 0\nwhile n < 10:\n    n = n + 1\n    if n == 3:\n        break\nprint(n, n < 10)\n",
 "finally_return": "def f():\n    try:\n        1/0\n    finally:\n        return 42\nprint(f())\n",
 "return_outside": "return\n",
 "clobber": "i = 'keep'\nfor i in range(3):\n    pass\nprint(i)\n",
 "t_pack": "t = 12345, 54321, 'hello!'\nprint(t)\n",
 "shadow_list": "list = [1, 2]\nlist('abc')\n",
 "walrus": "import io\nfile = io.StringIO('abcdefgh')\nwhile chunk := file.read(3):\n    print(chunk)\n",
 "walrus_old": "import io\nfile = io.StringIO('abcdefgh')\nwhile True:\n    chunk = file.read(3)\n    if not chunk:\n        break\n    print(chunk)\n",
 "import5": "import random\nrandom.seed(3)\nfor i in range(5):\n    print(random.randint(1, 10))\n",
 "multi": "import random, sys, os, math\nprint(random.__name__, sys.__name__, os.__name__, math.__name__)\n",
 "from_math": "from math import sqrt\nprint(sqrt(16))\nprint(math)\n",
 "as_math": "import math as m\nprint(m.sqrt(25))\nprint(m.__name__)\n",
 "star_pow": "print(pow(2, 3))\nfrom math import *\nprint(pow(2, 3))\n",
 "star_func": "def f():\n    from math import *\n",
 "seed": "import random\nrandom.seed(7)\nfirst = [random.randint(1, 20) for _ in range(5)]\nrandom.seed(7)\nsecond = [random.randint(1, 20) for _ in range(5)]\nprint(first == second)\n",
 "randint_ends": "import random\nrandom.seed(1)\nprint(sorted({random.randint(1, 3) for _ in range(200)}))\nprint(sorted({random.randrange(1, 3) for _ in range(200)}))\n",
 "modules_cache": "import sys\nprint('math' in sys.modules)\nimport math\nprint('math' in sys.modules)\n",
 "syspath0": "import sys\nprint(repr(sys.path[0]))\n",
 "warn_finally": "import warnings\nwith warnings.catch_warnings(record=True) as w:\n    warnings.simplefilter('always')\n    compile('for i in range(2):\\n    try:\\n        pass\\n    finally:\\n        break\\n', '<s>', 'exec')\nprint(len(w))\n",
 "unpack_ok": "x, y = (1, 2)\nprint(x, y)\n",
 "unpack_few": "x, y = (1,)\n",
 "for_pairs": "for i, v in enumerate(['tic', 'tac', 'toe']):\n    print(i, v)\n",
 "append": "a = [1, 2]\na.append(3)\nprint(a)\n",
 "list_set": "a = [1, 2]\na[0] = 99\nprint(a)\n",
 "tuple_set": "t = (1, 2)\nt[0] = 99\n",
 "str_set": "s = 'abc'\ns[0] = 'x'\n",
 "dict_ops": "users = {'Ada': 'active', 'Can': 'inactive'}\ndel users['Can']\nprint(users, len(users))\n",
 "iter_next": "it = iter([10, 20])\nprint(next(it))\nprint(next(it))\nprint(next(it))\n",
 "return_loop": "def first_even(items):\n    for x in items:\n        if x % 2 == 0:\n            return x\n    return None\nprint(first_even([1, 3, 4, 5]))\nprint(first_even([1, 3]))\n",
 "break_outside": "break\n",
 "continue_outside": "continue\n",
 "tryfinally_exc": "try:\n    int('x')\nfinally:\n    print('cleanup')\n",
 "finally_kb": "try:\n    raise KeyboardInterrupt\nfinally:\n    print('Goodbye, world!')\n",
 "dunder_main": "print(__name__)\n",
 "finally_ok": "try:\n    pass\nfinally:\n    for i in range(2):\n        break\n    def f():\n        return 1\n",
 "pathfirst_probe": "import sys\nprint(sys.path[0])\n",
 "while_not": "name = ''\nwhile not name:\n    name = input('>')\nprint(repr(name))\n",
}
GUESS = ("# This is a guess the number game.\nimport random\nsecret_number = random.randint(1, 20)\nprint('I am thinking of a number between 1 and 20.')\n"
 "# Ask the player to guess 6 times.\nfor guesses_taken in range(1, 7):\n    print('Take a guess.')\n    guess = int(input('>'))\n    if guess < secret_number:\n"
 "        print('Your guess is too low.')\n    elif guess > secret_number:\n        print('Your guess is too high.')\n    else:\n        break  # This condition is the correct guess!\n"
 "if guess == secret_number:\n    print('Good job! You got it in ' + str(guesses_taken) + ' guesses!')\nelse:\n    print('Nope. The number was ' + str(secret_number))\n")
RPS = ("import random, sys\nprint('ROCK, PAPER, SCISSORS')\n# These variables keep track of the number of wins, losses, and ties.\nwins = 0\nlosses = 0\nties = 0\n"
 "while True:  # The main game loop\n    print('%s Wins, %s Losses, %s Ties' % (wins, losses, ties))\n    while True:  # The player input loop\n"
 "        print('Enter your move: (r)ock (p)aper (s)cissors or (q)uit')\n        player_move = input('>')\n        if player_move == 'q':\n            sys.exit()  # Quit the program.\n"
 "        if player_move == 'r' or player_move == 'p' or player_move == 's':\n            break  # Break out of the player input loop.\n        print('Type one of r, p, s, or q.')\n"
 "    # Display what the player chose:\n    if player_move == 'r':\n        print('ROCK versus...')\n    elif player_move == 'p':\n        print('PAPER versus...')\n    elif player_move == 's':\n        print('SCISSORS versus...')\n"
 "    # Display what the computer chose:\n    move_number = random.randint(1, 3)\n    if move_number == 1:\n        computer_move = 'r'\n        print('ROCK')\n    elif move_number == 2:\n        computer_move = 'p'\n        print('PAPER')\n"
 "    elif move_number == 3:\n        computer_move = 's'\n        print('SCISSORS')\n    # Display and record the win/loss/tie:\n    if player_move == computer_move:\n        print('It is a tie!')\n        ties = ties + 1\n"
 "    elif player_move == 'r' and computer_move == 's':\n        print('You win!')\n        wins = wins + 1\n    elif player_move == 'p' and computer_move == 'r':\n        print('You win!')\n        wins = wins + 1\n"
 "    elif player_move == 's' and computer_move == 'p':\n        print('You win!')\n        wins = wins + 1\n    elif player_move == 'r' and computer_move == 'p':\n        print('You lose!')\n        losses = losses + 1\n"
 "    elif player_move == 'p' and computer_move == 's':\n        print('You lose!')\n        losses = losses + 1\n    elif player_move == 's' and computer_move == 'r':\n        print('You lose!')\n        losses = losses + 1\n")
PG["guess"] = GUESS
PG["guess16"] = GUESS.replace("secret_number = random.randint(1, 20)", "secret_number = 16")
PG["rps"] = RPS
PG["rps_paper"] = "import random\nrandom.randint = lambda a, b: 2\n" + RPS

# (id, label or None for the camel-case label, level, parent, leaf, paras)
# leaf = None for levels 1 and 2, else (example label, definition, io-example or None)
NODES = [
 ("Repetition", None, 1, None, None, [
  (W, "Repetition is the ability of a program to run the same block of code more than once, and it is the subject of the first half of chapter 3. Chapter 2 showed how a program chooses between blocks, so that some lines run and others are skipped; this chapter adds the loop, a statement that sends execution back to the start of a block so that the same lines can serve many values [[SW]]."),
  (Y, "Without repetition a program could do no more work than the lines its author typed out, whereas a loop lets the same few lines handle five items or five million. The book puts it directly: Python's two kinds of loops, while and for, open up the full power of automation because they can run lines of code millions of times per second [[SW]]. Almost every useful program in the rest of the course is built around at least one loop."),
  (H, "The branch is organised around the question of what decides when a loop stops. The sections on loop basics define the loop and its iteration, the condition loop stops when a test becomes false, the counted loop stops when a sequence runs out, and the section on loops in programs combines them into the two complete programs of the chapter, Guess the Number and Rock, Paper, Scissors."),
  (K, "Most loop mistakes are mistakes about stopping. A loop that never stops, a loop that stops one pass too early or too late, and a loop that never starts are all caused by a misjudged condition or a misjudged count, so each section below ends with the ways its loop can go wrong."),
 ], None),
 ("LoopBasics", "Loop basics", 2, "Repetition", None, [
  (W, "The loop basics are the two ideas on which every loop statement rests: the loop itself, which is a block that Python runs again and again, and the iteration, which is one run of that block. The two words are used constantly in the book and in Python's documentation, so they are defined before the particular loop statements are introduced."),
  (Y, "Separating the two ideas gives us a precise way to talk about a program. We can say that a loop executes its block once per iteration, that this loop made five iterations, or that a bug appears on the third iteration, and each of these statements is a claim that can be checked by running the program."),
  (H, "The next two sections define the loop and the iteration in turn. They use the book's own comparison of an if statement with a while statement, because the only difference between the two is whether execution jumps back to the start of the block."),
 ], None),
 ("Loop", None, 3, "LoopBasics", ("the if and while versions of the same block", "A loop is a block that Python runs repeatedly: at the end of the block, execution jumps back to the start instead of moving on.", None), [
  (W, "A loop is a statement that makes Python execute a block of code over and over. Python has two kinds, the while loop and the for loop, and each is written as a line that ends with a colon followed by an indented block, which the book calls the loop's clause [[SW]]. Where the if statement of chapter 2 decides whether a block runs, a loop decides how often it runs."),
  (Y, "Repetition is what turns a short list of instructions into a program that scales. The same lines can ask a question until the answer is usable, walk through every item of a collection, or count up to a limit, and the author writes them only once. Because nearly every later program contains a loop, the precise meaning of jumping back to the start has to be clear before anything else is built on it."),
  (E, "Loops appear whenever a program must do something an unknown or large number of times: checking what a user has typed, processing each item of a collection, retrying an action or running a game until the player quits. The chapter's two example programs, Guess the Number and Rock, Paper, Scissors, are both built from loops, and the second contains one loop inside another [[SW]]."),
  (H, "The book compares two snippets that differ only in one word. Both set spam to 0, test spam < 5, print Hello, world. and add one to spam, but the if version prints the message once, because at the end of an if clause execution continues after the statement, while the while version prints it five times, because at the end of a while clause execution jumps back to the start of the statement [[SW]]. Running both programs confirms the difference: the if version prints one line and the while version five."),
  (K, "A loop whose block changes nothing that its test looks at never ends. In the while snippet above, the line that adds one to spam is what finally makes spam < 5 false; a version of the program without that line keeps going until it is interrupted from outside, which the check below confirms by running it with a time limit."),
 ]),
 ("Iteration", None, 3, "LoopBasics", ("the five iterations of the while example", "One execution of a loop's block; a while loop tests its condition at the start of every iteration.", None), [
  (W, "An iteration is a single execution of a loop's block. A loop that runs its block five times is said to make five iterations, and the book uses the word in exactly this sense when it explains that the condition of a while loop is checked at the start of each iteration, that is, each time the loop is executed [[SW]]."),
  (Y, "Counting iterations is the way we reason about a loop: how many there will be, what changes from one to the next, and what the state of the program is when the last one finishes. The word also lets us describe a loop without naming its kind, because both the while loop and the for loop work iteration by iteration."),
  (E, "The word appears in the book's explanations of the while statement and of the for statement, in the documentation of continue, which continues with the next iteration of the loop [[PSF]], and in everyday talk about programs, as in the first iteration, the last iteration or an iteration that raised an error."),
  (H, "In a while loop each iteration begins by testing the condition, and the block runs only if the test is true. In a for loop each iteration begins by taking the next item from the sequence being walked through. With spam starting at 0 and the condition spam < 5, a counter placed in the block shows that the block runs five times, and a loop whose condition is false from the start makes no iteration at all, so the code after it simply runs next."),
  (K, "The number of iterations is not the same thing as the last value of a counter. After for i in range(5) has made its five iterations, the variable i holds 4, because counting started at 0, so a learner who expects 5 has confused the count with the final value."),
 ]),
 ("ConditionLoop", None, 2, "Repetition", None, [
  (W, "A condition loop is a loop whose length is decided by a test instead of by a count. The while statement is the loop of this kind, and the infinite loop is the special case in which the test can never fail [[SW]]."),
  (Y, "Many real tasks do not come with a known number of repetitions. A program that asks for a password until the right one arrives, or that plays a game until the player quits, cannot say in advance how long it will run, because the answer depends on what the user does. The condition loop is the tool made for these tasks."),
  (H, "Both sections of the group follow the same rule: the condition is evaluated at the start of every iteration, the block runs if the condition is true, and the loop ends the first time the condition is false. What differs is whether anything inside the loop can make the condition false, and the infinite loop shows what happens when nothing does."),
 ], None),
 ("WhileStatement", None, 3, "ConditionLoop", ("while name != 'your name':", "A while statement repeats its block as long as its condition is true, and tests the condition again after every pass.", None), [
  (W, "A while statement repeats its block for as long as its condition is true. In code it always consists of the while keyword, a condition, a colon and, starting on the next line, an indented block, which the book calls the while clause or while block [[SW]]. The condition is an expression, usually built with the comparison and logical operators of chapter 2, and the whole statement can be called a while loop or just a loop."),
  (Y, "The while statement is the loop for situations in which the data decides when to stop. The book's first example keeps asking the user to type, literally, the words your name, and it has no idea beforehand how many wrong answers will come before the right one. A loop that follows a test can express this directly, which a loop that follows a count cannot."),
  (E, "While loops appear in input checking, in game loops such as the main loop of Rock, Paper, Scissors, and in any program that repeats an action until some state has been reached. The language reference describes the statement as repeated execution as long as an expression is true, with an optional else clause that is run when the expression becomes false [[PSF]]."),
  (H, "At the start of every iteration Python evaluates the condition. If it is true, the block runs and execution jumps back to the condition; the first time it is false, the clause is skipped and the program continues after the loop [[SW]]. In the book's program the variable name is first set to the empty string so that name != 'your name' is true and the loop is entered; the input function inside the block then assigns a new value to name. When four attempts are typed, the last being your name, the prompt appears four times and the program ends with Thank you! The condition need not be a comparison: 0, 0.0 and the empty string count as false and every other value as true, so while not name: repeats until something non-empty has been typed [[SW]]."),
  (K, "There are three typical errors. If nothing in the block can make the condition false, the loop never ends. If the condition is false the very first time it is tested, the block never runs, which the check below shows by a loop that is skipped entirely. And if the variable in the condition has never been assigned, Python stops with a NameError before the first iteration, which is why the book's program begins by giving name a value."),
 ]),
 ("InfiniteLoop", None, 3, "ConditionLoop", ("while True:", "A loop whose condition never becomes false runs until something inside it leaves: break, return, sys.exit() or an exception.", None), [
  (W, "An infinite loop is a loop whose condition is always true, and the plainest form is while True. The expression True always evaluates to the value True, so the test at the top can never end the loop [[SW]]. The book is careful to say that an infinite loop that never exits is a common programming bug, but it also uses the form on purpose."),
  (Y, "A deliberate infinite loop is useful when the natural place to decide about stopping is in the middle of the block and not at its top. The book's second version of the name program asks first and tests afterwards, and the main loop of its Rock, Paper, Scissors game is also a while True loop, because a game should keep going until the player chooses to quit [[SW]]."),
  (E, "The form appears in yourName2.py, in swordfish.py, in the exit example and in both loops of the rock, paper, scissors program [[SW]]. In the wider world it is the shape of any program that waits for events, such as a menu that is shown again after every choice."),
  (H, "Because the test cannot end the loop, the loop can only be left from inside the block. The ways out are a break statement, a return statement that leaves the function containing the loop, a call to sys.exit() that ends the whole program, and an exception that nobody handles, and each of them has its own section in the group on loop control. In the check below a counter is increased on every pass and a break fires on the third, so the loop is left with the counter at 3."),
  (K, "A loop that was meant to end but cannot is a bug, and the program appears to hang or to print without end; a loop of this kind with an empty block never returns, which the check below shows by stopping it after a time limit. Whenever you write while True, make sure that at least one exit is reachable on every path through the block, and remember that Control-C stops a runaway program."),
 ]),
 ("CountedLoop", None, 2, "Repetition", None, [
  (W, "A counted loop is a loop whose number of iterations is fixed before it starts, because it walks through a sequence of values that already exists. The for statement is the loop of this kind, and the two sections that follow it show how it relates to the while loop and how a loop gathers a result [[SW]]."),
  (Y, "When the work is to be done once per item, or a given number of times, a counted loop spares the author the bookkeeping that a condition loop needs: no variable has to be set before the loop, tested in a condition and increased at the end of the block. The statement does that itself, and there is one less place for a mistake."),
  (H, "The for statement takes the values from an iterable, usually produced by the range function, and gives them to the loop variable one at a time. The following sections define the statement, show the while loop that is equivalent to it, and introduce the accumulator, the usual way of collecting a result across iterations."),
 ], None),
 ("ForStatement", None, 3, "CountedLoop", ("for i in range(5):", "A for statement takes each item of an iterable in turn, assigns it to its variable and runs the block once for each.", None), [
  (W, "A for statement runs its block once for each item of an iterable, assigning the item to its loop variable before each run. The book describes the statement as the for keyword, a variable name, the in keyword, a call to range() with up to three integers, a colon and an indented block [[SW]], and the language reference generalises it: the statement iterates over the elements of a sequence or of any other iterable object [[PSF]]."),
  (Y, "The for loop is the right tool whenever the work is to be done once per item or a fixed number of times. Because the number of iterations follows from the sequence, the author does not have to write a test or to maintain a counter, and the book therefore calls for loops more concise than the equivalent while loops [[SW]]."),
  (E, "The book's first for loop prints a message five times, its second adds up the integers from 0 to 100, and the Guess the Number program loops over a range of attempts. In ordinary programs the sequence is most often a list, a string or a dictionary rather than a range."),
  (H, "The language reference gives the exact order of events. The expression after in is evaluated once and must yield an iterable; Python creates an iterator for it; each item the iterator provides is assigned to the target and the block is executed; when the iterator has no more items the loop ends [[PSF]]. In the book's fiveTimes program the variable i is set to 0, 1, 2, 3 and 4 in turn, and the output is Hello!, five lines saying On this iteration, i is set to followed by the value, and Goodbye! [[SW]]."),
  (K, "Assigning to the loop variable inside the block does not change the iteration: the next item overwrites it, so the loop of the reference documentation that sets i = 5 still prints 0 to 9 [[PSF]]. The sequence must also be iterable; for i in 5 fails with a TypeError because an integer cannot be walked through, and the book's range(5) is what supplies five values."),
 ]),
 ("ForWhileEquivalence", None, 3, "CountedLoop", ("i = 0, while i < 5, i = i + 1", "A while loop with a counter set before the loop, tested in its condition and increased at the end of the block does what a for loop over a range does.", None), [
  (W, "The equivalent while loop is the rewriting of a for loop over a range as a while loop with an explicit counter. The counter is given its first value before the loop, the condition compares it with the limit, and the last line of the block increases it. The book presents the rewriting to show that for loops are just more concise and that a while loop can do the same thing [[SW]]."),
  (Y, "Writing the loop out by hand shows what the for statement does on our behalf. It exposes the three places in which a counting while loop can go wrong, namely the starting value, the test and the increase, and so it explains why the book recommends for loops for a specific number of times and while loops for as long as a particular condition is true [[SW]]."),
  (E, "The book rewrites fiveTimes.py in this way. The same transformation is useful when a for loop must be changed into a loop that can also stop for another reason, because the condition of a while loop can combine the counter with a second test."),
  (H, "The rewritten program starts with i = 0, repeats while i < 5, prints the same message and ends the block with i = i + 1. Run next to the for version it prints exactly the same text, from Hello! to Goodbye!, which the check below compares line by line [[SW]]."),
  (K, "The rewriting hides a trap that the for loop does not have. If a continue statement is placed before the line that increases the counter, the counter never changes once that branch has been taken, and the loop repeats the same iteration without end. In a for loop the same continue is harmless, because the statement takes the next item by itself, as the check below shows with both versions."),
 ]),
 ("Accumulator", None, 3, "CountedLoop", ("total = total + num", "A variable that starts at a known value before the loop and is updated on every iteration, so that it holds the running result when the loop ends.", ("sum(range(101))", "5050")), [
  (W, "An accumulator is a variable that collects a result across the iterations of a loop. It is given a known starting value before the loop, such as 0 for a sum, and every iteration updates it with the current item, as in total = total + num. When the loop ends, the variable holds the combined result."),
  (Y, "Many questions have the form combine all the items: the total of a list of prices, the number of guesses taken, the number of wins in a game. A loop by itself repeats work but forgets what it has done, so a variable outside the loop is needed to remember. The accumulator is the standard way to give a loop a memory."),
  (E, "The book's example is the story of the young Gauss, who was told to add the numbers from 0 to 100. The program sets total to 0, loops over range(101) and prints the result [[SW]]. The Rock, Paper, Scissors program uses three accumulators, wins, losses and ties, each increased by one when its case occurs."),
  (H, "The loop body total = total + num runs 101 times, once for each of the integers 0 to 100, and the printed result is 5,050. The book explains why: there are 50 pairs of numbers that add up to 101, and 50 times 101 is 5,050 [[SW]]. The built-in function sum, given the same range, returns the same total, because it performs the accumulation itself [[PSF]]."),
  (K, "The starting value belongs before the loop. If total = 0 is placed inside the block, it is reset on every iteration and the loop ends with only the last item, which for this range is 100. If the starting value is missing altogether, the first update fails with a NameError, because total + num needs a total that does not yet exist. The range must also be right: range(100) stops at 99 and gives 4,950."),
 ]),
 ("LoopComposition", "Loops in programs", 2, "Repetition", None, [
  (W, "Loops in programs are the ways in which loops are combined with the other statements of the chapter into working code: a loop placed inside another loop, and the two complete programs of the chapter, Guess the Number and Rock, Paper, Scissors [[SW]]."),
  (Y, "Knowing each statement separately is not yet programming. The book therefore ends the chapter by showing, line by line, how a counted loop with an early exit forms a guessing game and how two nested condition loops form a game that runs until the player quits, and it says that these programs show how everything learned so far comes together [[SW]]."),
  (H, "The group starts with the nested loop, since the second program needs it, and then reads the two programs from top to bottom. For each program the sections below run the real source with scripted input, so that every output that is quoted has actually been produced."),
 ], None),
 ("NestedLoop", None, 3, "LoopComposition", ("a while loop inside a while loop", "A loop placed in the block of another loop: the inner loop runs completely on every iteration of the outer one, and break leaves only the inner loop.", None), [
  (W, "A nested loop is a loop that is placed inside the block of another loop. The outer loop starts an iteration, the inner loop then runs from its beginning to its end, and only afterwards does the outer loop continue with its next iteration. The book's Rock, Paper, Scissors program contains a while loop inside another while loop [[SW]]."),
  (Y, "Nesting lets a program express two levels of repetition in one structure: games and rounds, rows and columns, items and their parts. It also lets a small loop guard a step of a larger one, as the second loop of the book's game does when it keeps asking until the player has typed a valid move."),
  (E, "In the book's game the first loop is the main game loop, in which a single game is played on each iteration, and the second is the player input loop, which asks for input and keeps looping until the player has entered r, p, s or q [[SW]]. Nested counted loops are used for tables, grids and every comparison of each item with each other item."),
  (H, "The number of times the innermost block runs is the product of the iteration counts: an outer loop of 4 iterations around an inner loop of 3 runs the inner block 12 times in all. A break statement leaves only the innermost loop that contains it, so when the inner loop of the example breaks at j equal to 1, the outer loop goes on to its next value of i, and the output is 0 0 and 1 0 [[PSF]]. This is exactly how the book's input loop works: break leaves the player input loop and sends control to the code that shows the moves, while the main game loop continues."),
  (K, "A break does not end the whole structure, and a learner who needs to leave both loops must use another means such as sys.exit(), which the book's game uses for the quit command. The cost of nesting also grows quickly, since a loop of 1,000 iterations inside another of 1,000 runs its block a million times."),
 ]),
 ("GuessTheNumber", None, 3, "LoopComposition", ("guessTheNumber.py", "A program that imports random, picks a secret number and gives the player at most six guesses in a for loop that ends early with break.", None), [
  (W, "Guess the Number is the first complete program of the chapter, a game in which the computer picks a secret number between 1 and 20 and the player has six chances to find it, receiving the hint too low or too high after each wrong guess [[SW]]. It combines an import statement, a call to random.randint(), a for loop over range(1, 7), conversions with int() and str(), an if, elif and else chain, and a break."),
  (Y, "The program shows how little is needed to build something interactive. It also shows a design that is worth remembering: a counted loop that gives a limit on the number of attempts, and a break that leaves the loop early when the goal has been reached, so that one loop handles both the success and the failure of the player."),
  (E, "The program appears in the book as guessTheNumber.py, and the same structure, a limited number of tries with an early exit on success, is the shape of password prompts, retry logic and many small games. The book also points to The Big Book of Small Python Projects for more programs of this kind [[SW]]."),
  (H, "The secret number is chosen once, before the loop. In each iteration the program asks for a guess, converts the text returned by input() with int(), and compares it with the secret; a correct guess runs break, and the code after the loop tests guess == secret_number to decide between the success message and the message that gives away the number [[SW]]. With the secret fixed at 16 and the guesses 10, 15, 17 and 16 typed in, the program prints Good job! You got it in 4 guesses! and with six low guesses it prints Nope. The number was 16, with no full stop after the number because the program does not print one. The variables guesses_taken and guess are still available after the loop, which the final message relies on."),
  (K, "The program trusts the player. If the text typed cannot be converted, as with abc, int() raises a ValueError and the program stops. The secret number must be drawn before the loop, because a call to random.randint() inside the loop would choose a new number for every guess. Finally, the program always reports the number of guesses with the word guesses, even after a single guess."),
 ]),
 ("RockPaperScissors", None, 3, "LoopComposition", ("rpsGame.py", "A program built from two nested while True loops: an input loop that keeps asking until the move is valid, and a main loop that plays one game per iteration.", None), [
  (W, "Rock, Paper, Scissors is the second complete program of the chapter. The player types r, p or s, the computer chooses a move at random, the program announces who has won, and a running score of wins, losses and ties is printed before every game; typing q ends the program [[SW]]."),
  (Y, "The program brings together nearly everything in the chapter: an import of two modules, three accumulators, two nested while True loops, break to leave the input loop, sys.exit() to leave the program, and long chains of if and elif statements. It shows that an infinite loop with deliberate exits is the natural shape for a program that waits for a user."),
  (E, "The structure of an outer loop that runs one round per iteration and an inner loop that validates the input of that round is common in menus, games and command interpreters. The book explains the program in pieces, starting with the imports and the three variables that keep the score, and then each part of the two loops [[SW]]."),
  (H, "The inner loop prints the prompt, reads a move and acts on it: q calls sys.exit(), a valid move breaks out of the loop, and anything else prints Type one of r, p, s, or q. and loops again. The program then draws random.randint(1, 3) and turns the number into a move. If the computer's choice is forced to be paper, a run in which the player types p, then q, prints PAPER versus..., PAPER and It is a tie!, after which the score line reads 0 Wins, 0 Losses, 1 Ties [[SW]]. The score line is built with %s placeholders filled from a tuple, and an f-string from chapter 1 produces the same text."),
  (K, "The nine combinations of moves are written out by hand as an elif chain, and a slip in any one of them gives a wrong verdict. The program also has no way to leave the main loop other than the quit command, so every ending goes through sys.exit(). Finally, the input loop only checks the single letters, which is why anything else, such as x, is rejected with the reminder and not with an error."),
 ]),
 ("Sequence", None, 1, None, None, [
  (W, "In chapter 3 the word sequence stands for whatever a for loop can walk through. Python's glossary gives the strict meaning: a sequence is an iterable that supports efficient access to its elements through integer indices and that has a length, and the built-in sequence types include list, str, tuple and bytes [[PSF]]. This branch of the chapter collects the supplies of values for loops, namely the range, the helpers enumerate and zip, the iteration protocol that every for loop obeys and the collection values that loops most often traverse."),
  (Y, "A for statement is only as useful as the values it is given. The loops of the book walk through a range of integers, but the loops of real programs walk through lists of records, lines of text, the keys of a dictionary or the results of a calculation. Knowing the available supplies, and how each one behaves when it is walked through, is what lets a learner choose the right one."),
  (H, "The branch moves from the concrete to the general. The range sequence is the supply that the book uses, the iteration helpers extend what a loop can see in each iteration, the iteration protocol explains what Python does behind every for statement, and the collection values name the containers whose contents are most often walked through."),
  (K, "Not everything that a loop can walk through is a sequence. A dictionary can be looped over although the glossary classes it as a mapping, because its lookups use keys and not integer positions, and an iterator can be consumed only once [[PSF]]. The sections of the branch point out these differences where they matter."),
 ], None),
 ("RangeSequence", None, 2, "Sequence", None, [
  (W, "A range sequence is the arithmetic progression of integers that the built-in range produces. The Python tutorial describes the function as one that generates arithmetic progressions, and the reference documentation adds that range is really an immutable sequence type, one whose contents cannot be changed after it is created, and not a function [[PSF]]. The group covers the forms of the call and the properties of the result."),
  (Y, "Counting is the most common reason to loop, and range is Python's way of counting. Learning its three forms, with a stop value, with a start and a stop, and with a step, makes it possible to loop forwards, backwards and in strides without writing a counter by hand. Learning its other properties explains why it can stand for a very long sequence at almost no cost."),
  (H, "The group first takes the four forms of the call: stop only, start and stop, with a step, and counting down. It then explains that a range is lazy, that its end point is excluded by design, and that it supports the usual operations of a sequence, such as the length, membership tests and indexing."),
 ], None),
 ("RangeStop", None, 3, "RangeSequence", ("range(5)", "range(n) yields the integers from 0 up to but not including n.", ("list(range(5))", "[0, 1, 2, 3, 4]")), [
  (W, "Called with a single argument, range(stop) stands for the whole numbers 0, 1, 2 and so on up to the number just before stop. The tutorial puts it this way: the given end point is never part of the generated sequence, and range(10) generates 10 values, which are the legal indices for the items of a sequence of length 10 [[PSF]]. The book teaches the call in this form first, in the loop for i in range(5) [[SW]]."),
  (Y, "Doing something n times is the most frequent kind of loop, and for i in range(n) is the usual way to write it. Starting at 0 is not an accident: the values range(n) produces are exactly the positions of the items of a sequence of n items, so the same expression serves for counting and for indexing."),
  (E, "The form is met in the book's fiveTimes program, in the sum over range(101), and in many programs that repeat an action a fixed number of times. The reference documentation notes that range represents immutable arithmetic sequences of integers, so that iterating range(3) yields 0, 1 and then 2 [[PSF]]."),
  (H, "For a positive step the contents of a range r are given by the formula r[i] = start + step * i, for i from 0 while r[i] < stop, and with only a stop given the start is 0 and the step is 1 [[PSF]]. Hence list(range(5)) is [0, 1, 2, 3, 4], len(range(5)) is 5, and range(0) is empty. The book's answer to its third practice question follows from the same formula: range(10), range(0, 10) and range(0, 10, 1) describe the same values [[SW]]."),
  (K, "The classic mistake is to expect the end point to be included, so that range(5) is imagined to contain 5; it has five values, and the last is 4. The arguments must be integers, and range(2.5) raises a TypeError saying that a float cannot be interpreted as an integer."),
 ]),
 ("RangeStartStop", None, 3, "RangeSequence", ("range(12, 16)", "range(start, stop) begins at start and ends before stop.", ("list(range(12, 16))", "[12, 13, 14, 15]")), [
  (W, "With two arguments, range(start, stop) begins at start and ends just before stop. The book introduces it as the way to follow any sequence of integers, including one that starts at a number other than zero, and shows that for i in range(12, 16) prints 12, 13, 14 and 15 [[SW]]."),
  (Y, "Many counts do not begin at zero: the years of a period, the lines of a page, the numbers 1 to 10 for people who count from one. The two-argument form makes the first value explicit, so that the loop says what it covers and the author does not have to adjust a zero-based counter by adding one."),
  (E, "The Guess the Number program counts its attempts with range(1, 7), so that the variable that remembers the number of guesses starts at 1, the number a player would say for the first guess [[SW]]. Date and score tables and numbered listings use the same form."),
  (H, "The first argument is the value at which the loop variable starts, and the second is the number up to, but not including, which it runs [[SW]]. The number of values is therefore stop minus start: range(12, 16) holds 4 values. If stop is not greater than start, the range is empty, so list(range(16, 12)) is an empty list and a loop over it makes no iteration at all [[PSF]]."),
  (K, "The order of the arguments matters, and the reversed order does not raise an error; it simply yields nothing, which can look like a loop that is skipped. To count down, a third argument with a negative value is needed, as the section on descending ranges shows."),
 ]),
 ("RangeStep", None, 3, "RangeSequence", ("range(0, 10, 2)", "A third argument is the step between values.", ("list(range(0, 10, 2))", "[0, 2, 4, 6, 8]")), [
  (W, "A third argument to range is the step, the amount by which the value is increased after each iteration. The call range(0, 10, 2) therefore counts from 0 to 8 in intervals of two, and the book shows that its loop prints 0, 2, 4, 6 and 8 [[SW]]. If the step is omitted it is 1 [[PSF]]."),
  (Y, "Striding through the values lets a loop visit every second item, every tenth year or every multiple of some number without testing each value in the loop body. The step turns a filter that the author would have to write into a property of the sequence itself."),
  (E, "Steps are used for even and odd numbers, for tables in which the entries are spaced regularly and for indices of grouped data. The tutorial's own examples are list(range(0, 10, 3)), which is [0, 3, 6, 9], and a step of -30 in the range from -10 to -100 [[PSF]]."),
  (H, "The formula r[i] = start + step * i still applies, so the values are start, start plus one step, start plus two steps and so on, as long as they stay below stop. For range(0, 10, 3) the values are 0, 3, 6 and 9, and the length is 4, since the next value, 12, would pass the end point [[PSF]]."),
  (K, "A step of zero would never leave the first value, so Python refuses it: range(0, 10, 0) raises a ValueError with the message range() arg 3 must not be zero. The end point stays excluded even when the step lands on it, which is why range(0, 10, 2) stops at 8 and not at 10."),
 ]),
 ("RangeDescending", None, 3, "RangeSequence", ("range(5, -1, -1)", "A negative step counts down, and the stop value is still excluded.", ("list(range(5, -1, -1))", "[5, 4, 3, 2, 1, 0]")), [
  (W, "A negative step makes a range count down instead of up. The book's example for i in range(5, -1, -1) prints the numbers from five down to zero, and it describes the negative step as the way to make the for loop count down [[SW]]. The end point is excluded as always, which is why the stop value is -1 and not 0."),
  (Y, "Counting down is needed for countdowns, for scanning a sequence from its end towards its beginning and for removing items from the back first. A negative step expresses it in one argument and keeps the loop in the same readable form as a loop that counts up."),
  (E, "The form appears in the book's fifth range example, and in the tutorial's list(range(-10, -100, -30)), which is [-10, -40, -70]. For an existing sequence the tutorial recommends a different tool, the reversed function: for i in reversed(range(1, 10, 2)) visits 9, 7, 5, 3 and 1 [[PSF]]."),
  (H, "For a negative step the contents of the range are still given by start + step * i, but the condition is that the value stays greater than stop, and not less than it [[PSF]]. In range(5, -1, -1) the values are 5, 4, 3, 2, 1 and 0, and the next value, -1, equals stop and is excluded."),
  (K, "The default step is positive, so range(5, 0) is empty: it asks Python to count up from 5 towards 0, which it cannot do. A learner who wants to count down must always give the negative step, and must remember that the stop value is one beyond the last number wanted."),
 ]),
 ("LazyRange", None, 3, "RangeSequence", ("range(10)", "A range is an object that produces its values when iterated, not a list holding them.", ("range(10)", "range(0, 10)")), [
  (W, "A range is lazy: it does not store its values but produces them when they are asked for. The tutorial shows that printing range(10) displays range(0, 10) and explains that the object behaves in many ways as if it were a list, but in fact it isn't; it returns the successive items of the desired sequence when you iterate over it, without really making the list, thus saving space [[PSF]]. The library documentation uses the word lazy in the same sense for zip, whose elements are not processed until the iterable is iterated on [[PSF]]."),
  (Y, "Laziness is why for i in range(1000000) does not need space for a million integers. The reference documentation states the advantage: a range object always takes the same small amount of memory, however large the range is, because it stores only the start, stop and step values and calculates individual items as needed [[PSF]]."),
  (E, "The consequences are visible whenever a range is printed or compared. The shell shows only range(0, 10), and a range is not equal to a list that holds the same values. The functions that take an iterable, such as sum, work on it directly: sum(range(4)) is 6, the tutorial's own example [[PSF]]."),
  (H, "A range keeps only three numbers, and each value is computed from them when needed. Two ranges of very different lengths therefore occupy the same space, and a list is built only when one is asked for, as in list(range(10)). A range can also be walked through any number of times, because each loop starts a fresh pass over the same three numbers."),
  (K, "A range is not a list, however similar it looks. Comparing range(10) with the list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] gives False, and the type check isinstance(range(3), list) gives False too. If a real list is needed, for example to see the values or to change them, the range has to be converted with list()."),
 ]),
 ("HalfOpenRange", "Half-open range", 3, "RangeSequence", ("range(0, 24) for the hours of a day", "A range includes its start and excludes its end, so its length is stop minus start and neighbouring ranges join without a gap.", ("len(range(0, 24))", "24")), [
  (W, "Python writes ranges in the closed, open format: the start is included and the end is excluded. The book explains in a separate box why the loop goes up to but not including the number given, and says that in programming ranges are often specified in this way because it leads to fewer bugs [[SW]]. A range of this kind is called half-open."),
  (Y, "The book gives the reasons. The size of the range is just the end minus the start, so the range 0, 10 holds 10 - 0 = 10 numbers, whereas a closed, closed range such as 0, 9 needs the calculation 9 - 0 + 1, which is easily mistaken for 9 - 0 - 1, an off-by-one error. The start of the next range is simply the end of the previous one [[SW]]."),
  (E, "The convention appears in range itself and in slices, which cut a part out of a sequence by writing two positions in square brackets with a colon between them, where 'hello'[1:3] is 'el' because the end position is not included. The book's example is a day of timestamps: the half-open range from 00:00:00 to 24:00:00.0 is much easier to work with than the closed range 00:00:00 to 23:59:59.999, and in the same spirit range(0, 24) holds the 24 hours of a day [[SW]]."),
  (H, "Because the end is excluded, len(range(a, b)) is b - a, and two ranges that meet at a point fit together: the values of range(0, 5) followed by those of range(5, 10) are exactly the values of range(10). The tutorial adds that range(10) holds the legal indices of a sequence of length 10 [[PSF]]."),
  (K, "The convention takes getting used to; the book says that closed, open ranges may seem odd at first but become second nature with experience [[SW]]. When the last number must be included, the end point has to be one larger: list(range(1, 11)) holds 1 to 10, the example in the library documentation [[PSF]]."),
 ]),
 ("RangeOperations", "Range operations", 3, "RangeSequence", ("range(0, 20, 2)[5]", "A range supports length, membership tests, indexing, slicing and index lookup, but not concatenation or repetition.", ("range(0, 20, 2)[5]", "10")), [
  (W, "A range is a full sequence and supports most of the operations that lists and strings have. The library documentation lists length, membership tests with in, indexing with positive and negative positions, slicing and index lookup, and says that ranges implement all of the common sequence operations except concatenation and repetition [[PSF]]."),
  (Y, "These operations let a program ask questions of a range without looping over it: how many values it holds, whether a number belongs to it, which value stands at a given position. They also make a range a good model of the sequences that come later in the course, since it shows what a sequence is able to do."),
  (E, "The documentation's example is r = range(0, 20, 2). Then 10 in r is True and 11 in r is False, r[5] is 10, r.index(10) is 5, r[-1] is 18, and the slice r[:5] is again a range, range(0, 10, 2) [[PSF]]. A range also exposes the numbers it stores as the attributes start, stop and step."),
  (H, "Membership of an integer is decided by computation, not by walking through the values, since the range knows its start, stop and step; the documentation says that int objects are tested for membership in constant time. Slicing a range returns a range, so the result is as lazy as the original [[PSF]]."),
  (K, "The operations that would break the strict pattern of a range are missing. Joining two ranges with + raises a TypeError, because the result would usually not be an arithmetic progression, and the same holds for repetition with *. To combine ranges, convert them to lists first."),
 ]),
 ("IterationHelper", None, 2, "Sequence", None, [
  (W, "Iteration helpers are built-in functions that wrap an iterable so that a loop sees more than its plain items. The group of the chapter has two of them: enumerate adds a running count to each item, and zip walks through several iterables side by side. The Python tutorial presents both in its section on looping techniques [[PSF]]."),
  (Y, "Beginners often reach for range(len(a)) and an index when they need a position or a second sequence, and the resulting code is harder to read and easier to get wrong. The helpers say what is meant directly: give me the items with their positions, or give me these items together."),
  (H, "Each helper returns an iterator, an object that supplies its values one at a time, and the for statement consumes it like any other iterable. The sections on enumerate and zip show the pairs that they produce, and the section on unpacking explains how a loop receives each pair in two variables."),
 ], None),
 ("EnumerateFunction", None, 3, "IterationHelper", ("enumerate(['tic', 'tac', 'toe'])", "enumerate pairs each item with a running count, replacing range(len(a)) when both are needed.", ("list(enumerate(['tic', 'tac', 'toe']))", "[(0, 'tic'), (1, 'tac'), (2, 'toe')]")), [
  (W, "The enumerate function takes an iterable and returns an iterator of pairs, each made of a count and the corresponding item. The library documentation shows list(enumerate(seasons)) giving [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')], and says that the count begins at start, which defaults to 0 [[PSF]]."),
  (Y, "A loop often needs both the position of an item and the item itself, for numbered output or to compare neighbours. The tutorial first shows how to do this with range and len, printing a[i] for every i in range(len(a)), and then says that in most such cases it is convenient to use the enumerate function [[PSF]]."),
  (E, "The tutorial's looping techniques give the standard form: for i, v in enumerate(['tic', 'tac', 'toe']): print(i, v), which prints 0 tic, 1 tac and 2 toe [[PSF]]. The form is met whenever a program numbers its output, reports the position of an error in a list or processes every second element."),
  (H, "Each pair is a tuple, and the for statement unpacks it into the two variables of the loop. The optional start argument changes the first count, so list(enumerate(['tic', 'tac', 'toe'], start=1)) is [(1, 'tic'), (2, 'tac'), (3, 'toe')]. The result of enumerate is an iterator and not a list; its type is enumerate, and next(enumerate('ab')) returns the first pair, (0, 'a'). The pairs equal those that the index-based loop builds."),
  (K, "The counting starts at 0 by default, which is right for positions but wrong for numbering that people read, such as a list of results beginning with 1; the start argument fixes that. Printing the enumerate object itself shows only an object description, so the values are seen by looping or by converting with list()."),
 ]),
 ("ZipStrict", None, 3, "IterationHelper", ("zip(a, b, strict=True)", "zip walks several iterables together; strict=True raises ValueError when their lengths differ instead of stopping at the shortest.", ("list(zip('ab', [1, 2], strict=True))", "[('a', 1), ('b', 2)]")), [
  (W, "The zip function walks through several iterables in parallel and produces tuples, the first holding the first item of each iterable, the second the second items, and so on [[PSF]]. Since Python 3.10 it takes an optional keyword argument strict, an argument that is written with its name; with strict=True the iterables must have the same length."),
  (Y, "Pairing two sequences is a daily task: names with scores, questions with answers, coordinates. The default behaviour has a weakness that PEP 618 describes: when the lengths differ, zip stops at the shortest and silently ignores the rest, so faulty refactoring or logic errors could easily result in silently losing data [[P618]]."),
  (E, "The tutorial pairs questions and answers with for q, a in zip(questions, answers) [[PSF]]. The strict form is useful wherever the iterables are assumed to have equal length, which the library documentation says is the usual case and for which it recommends strict=True [[PSF]]."),
  (H, "By default zip stops when the shortest iterable is exhausted, so list(zip('abc', [1, 2])) is [('a', 1), ('b', 2)] and the c is dropped without a word. With strict=True the same call raises a ValueError with the message zip() argument 2 is shorter than argument 1, and when the second iterable is the longer one the message ends with longer than argument 1. Equal lengths produce the same pairs as before. Like range, zip is lazy [[PSF]]."),
  (K, "The error is raised only when the mismatch is reached, after the pairs before it have been produced, so a loop may already have acted on some of them. And strict was added in Python 3.10, so a program that uses it does not run on older interpreters [[P618]]."),
 ]),
 ("TargetUnpacking", "Unpacking in a loop", 3, "IterationHelper", ("for i, v in enumerate(...):", "A loop variable list receives the parts of each item: a pair is unpacked into two names, and the number of names must match the number of parts.", None), [
  (W, "Unpacking is the assignment of the parts of a sequence to several variables at once. In a for statement the variable after the keyword for can be a list of names, and each item of the iterable is assigned to that list by the ordinary rules of assignment [[PSF]]. That is what makes for i, v in enumerate(items) work."),
  (Y, "Without unpacking, a loop over pairs would have to index each pair, writing pair[0] and pair[1], which hides the meaning of the parts. With two named variables the loop body reads as a sentence about an index and a value, a question and an answer, a key and a value."),
  (E, "Besides enumerate and zip, the same form serves for the items() method of a dictionary, which gives the key and the value of each entry [[PSF]]. In plain assignments it appears as a, b = (1, 2), which gives a the value 1 and b the value 2."),
  (H, "The tutorial calls the collection of values into a tuple packing and the reverse sequence unpacking, and notes that unpacking requires as many variables on the left as there are elements on the right; multiple assignment is a combination of the two [[PSF]]. For a tuple packed from 12345, 54321 and 'hello!' the printed form is (12345, 54321, 'hello!'). In a loop, the unpacking happens at the start of every iteration."),
  (K, "The counts must agree. Assigning a one-element tuple to two names raises a ValueError with the message not enough values to unpack (expected 2, got 1), and too many values raise a ValueError as well. The names are ordinary variables, so they keep their last values after the loop, as every loop variable does."),
 ]),
 ("IterationProtocol", "Iteration protocol", 2, "Sequence", None, [
  (W, "The iteration protocol is the agreement between a for loop and the objects it walks through. An object that can be walked through is an iterable; the loop asks it for an iterator; and the iterator hands out the items one at a time and announces when there are no more. Python's library documentation describes the agreement as two methods that together form the iterator protocol [[PSF]]."),
  (Y, "The protocol explains why one for statement works with a range, a list, a string, a dictionary or an enumerate object alike. It also explains behaviours that otherwise look like quirks, such as an iterator that is empty when it is walked through a second time."),
  (H, "The group defines the two roles in turn. The iterable is the thing that is looped over and the iterator is the thing that remembers the position in it. The for statement does all of the bookkeeping, creating the iterator and asking for items until it signals the end, so that ordinary programs rarely touch it directly."),
 ], None),
 ("IterableObject", "Iterable", 3, "IterationProtocol", ("for ch in 'abc':", "An iterable is an object that can return its members one at a time, so it can be the subject of a for loop.", ("list('abc')", "['a', 'b', 'c']")), [
  (W, "An iterable is an object capable of returning its members one at a time. Python's glossary lists the sequence types, such as list, str and tuple, and some other types such as dict and file objects as examples, and adds that iterables can be used in a for loop and in many other places where a sequence is needed, such as zip() and map() [[PSF]]."),
  (Y, "The idea is what lets one statement serve for so many sources. The for loop does not care whether its values come from a range, a list, a text or a file, as long as the source is iterable. A function that accepts any iterable is therefore more useful than one that accepts only lists."),
  (E, "Walking through a string visits its characters, so list('abc') is ['a', 'b', 'c']; walking through a dictionary visits its keys, so list({'a': 1, 'b': 2}) is ['a', 'b']; walking through a range visits its integers. The tutorial calls the range an object that is iterable, that is, suitable as a target for functions and constructs that expect something from which they can obtain successive items until the supply is exhausted [[PSF]]."),
  (H, "Passed to the built-in function iter(), an iterable returns an iterator, which is good for one pass over the values. The for statement does this automatically, creating a temporary unnamed variable to hold the iterator for the duration of the loop [[PSF]]. A list, for instance, gives a list iterator, and a range gives a range iterator; each pass over a container starts from a fresh iterator."),
  (K, "Not every object is iterable. Calling iter(5), which is what for i in 5 does behind the scenes, raises a TypeError saying that an int object is not iterable. A beginner who writes for i in 5 meant for i in range(5)."),
 ]),
 ("IteratorObject", "Iterator", 3, "IterationProtocol", ("next(iter('hello'))", "An iterator is an object that supplies the items of an iterable one at a time through next() and raises StopIteration when none are left.", ("next(iter('hello'))", "'h'")), [
  (W, "An iterator is an object representing a stream of data. According to the glossary, repeated calls to its __next__() method, or passing it to the built-in function next(), return successive items of the stream, and when no more data are available a StopIteration exception is raised instead [[PSF]]. At that point the iterator is exhausted."),
  (Y, "The iterator is the part that remembers where the loop is. It lets a for statement process data that does not exist all at once, such as the lines of a long file or the values of a range, and it is the reason a loop can stop cleanly: the end of the data is a signal and not a guess."),
  (E, "Iterators come from iter(), and many built-ins return them directly, among them enumerate, zip and reversed. The for statement uses one in every loop. The same object can be driven by hand: with it = iter([10, 20]), next(it) gives 10, a second call gives 20, and a third raises StopIteration."),
  (H, "The protocol requires two methods, __iter__(), which returns the iterator itself, and __next__() [[PSF]]. Because the iterator returns itself, every iterator is also an iterable, whereas a list returns a new iterator every time. The call next(it, default) returns the default instead of raising when the iterator is exhausted, so next(iter([]), 'done') is 'done'."),
  (K, "An iterator can be used only once. After list(it) has consumed iter([1, 2]), a second list(it) gives an empty list, which makes the iterator look like an empty container [[PSF]]. A learner who stores the result of enumerate or zip and loops over it twice will find the second loop silent. And a list is iterable but is not an iterator itself, so next([1, 2]) raises a TypeError saying that a list object is not an iterator; iter([1, 2]) has to be called first."),
 ]),
 ("CollectionValue", "Collection value", 2, "Sequence", None, [
  (W, "A collection value is a value that holds other values. The chapter touches four of them: the sequence in general, the list, the tuple and the dictionary. The Python tutorial treats lists, tuples and dictionaries in its chapter on data structures [[PSF]]."),
  (Y, "Loops are written to process collections, and the book's own loops reach for them as soon as the examples become realistic. The tutorial's advice on changing a collection while looping over it, which the section on hazards takes up, talks of lists and dictionaries, so these have to be understood first."),
  (H, "Each of the four sections below says what the collection is, how its members are reached and what a loop over it produces. The full treatment of each type belongs to the chapters that follow; the sections give only what chapter 3 itself uses."),
 ], None),
 ("SequenceKind", "Sequence type", 3, "CollectionValue", ("'hello'[1]", "A sequence is an ordered collection whose members are reached by integer position, counted from 0, and which has a length.", ("'hello'[1]", "'e'")), [
  (W, "A sequence is an ordered collection whose members have positions. The glossary defines it as an iterable that supports efficient element access using integer indices and that has a length, and names list, str, tuple and bytes among the built-in sequence types [[PSF]]. The library documentation adds range as the third basic sequence type besides lists and tuples [[PSF]]."),
  (Y, "Knowing that strings, lists, tuples and ranges are all sequences means that what is learned about one carries over to the others: they can be indexed, measured with len, sliced and looped over in the same way. A for loop over a string behaves like a for loop over a list of its characters."),
  (E, "Positions start at zero, as the glossary points out in its entry for index [[PSF]]. So 'hello'[1] is 'e', [10, 20, 30][0] is 10, and (10, 20, 30)[-1] is 30, because a negative position counts from the end. The function len gives the length, as chapter 1 showed for strings."),
  (H, "A sequence is reached by integer positions, which is what separates it from a mapping, whose members are reached by keys. A for loop over a sequence gives the members in order of position, which is why enumerate can number them and why the order of a list is predictable."),
  (K, "A dictionary looks similar, since it also supports lookup with square brackets and has a length, but the glossary classes it as a mapping because its lookups use arbitrary hashable keys (values with a fixed content that Python can turn into a lookup number) and not integers [[PSF]]. Asking a dictionary for position 0 raises a KeyError unless 0 happens to be a key."),
 ]),
 ("ListValue", "List", 3, "CollectionValue", ("[10, 20, 30]", "A list is a mutable sequence written between square brackets; its items can be replaced, added and removed.", ("list(range(3)) + [9]", "[0, 1, 2, 9]")), [
  (W, "A list is an ordered collection written with its items between square brackets and separated by commas. The reference documentation describes the type as a mutable sequence [[PSF]], and the glossary adds that, despite its name, a list is more akin to an array in other languages than to a linked list, since access to its elements is fast [[PSF]]."),
  (Y, "Lists hold the data that programs process: names, prices, lines, results. Most loops outside of textbooks walk through a list, and most programs build a list as they go. Because a list can change, it is also the collection for which the hazard of editing while looping arises."),
  (E, "The chapter meets lists in the call list(range(5)), which turns a range into a visible list, in the tutorial examples of enumerate and zip, and in the hazard of removing items while looping. Joining two lists with + gives a new list, so list(range(3)) + [9] is [0, 1, 2, 9]."),
  (H, "Items are reached by position, like those of any sequence, and can be changed in place. The method append adds an item at the end, so after a = [1, 2] and a.append(3) the list is [1, 2, 3], and an assignment such as a[0] = 99 replaces an item [[PSF]]. A for loop over a list gives the items in order."),
  (K, "A list is mutable, which means that its contents can be changed in place after it has been created, so two names can refer to the same list and a change through one is seen through the other. A string or a tuple does not allow item assignment; trying it raises a TypeError, which is why a list is the right choice when the collection must change."),
 ]),
 ("TupleValue", "Tuple", 3, "CollectionValue", ("(0, 'tic')", "A tuple is an immutable sequence of values separated by commas, usually written in parentheses; enumerate and zip produce their pairs as tuples.", ("tuple(range(3))", "(0, 1, 2)")), [
  (W, "A tuple is a sequence of values separated by commas, and on output it is always shown in parentheses. The tutorial describes tuples as immutable and usually containing a heterogeneous sequence of elements that are accessed via unpacking or indexing [[PSF]]."),
  (Y, "A tuple is the natural container for a small group of values that belong together, such as a count and an item or a name and a score. Because it cannot change, a tuple can be handed around without the risk that someone else alters it."),
  (E, "In this chapter tuples appear as the pairs produced by enumerate and zip: list(enumerate('ab')) is [(0, 'a'), (1, 'b')]. They also appear as the values filled into the percent placeholders of the book's score line, and as the result of tuple(range(3)), which is (0, 1, 2)."),
  (H, "A tuple is indexed like any sequence, so (0, 'tic')[0] is 0, and it is unpacked into names by assignment. Trying to assign to one of its items raises a TypeError with the message 'tuple' object does not support item assignment, the tutorial's own example [[PSF]]."),
  (K, "A tuple with one item needs a trailing comma, because parentheses alone do not make a tuple. ('hello',) has length 1, while ('hello') is just the string, and the empty tuple () has length 0 [[PSF]]. A forgotten comma is a quiet error, since no exception is raised."),
 ]),
 ("DictionaryValue", "Dictionary", 3, "CollectionValue", ("{'Ada': 'active', 'Can': 'inactive'}", "A dictionary is a collection of key and value pairs written between braces; a value is looked up by its key.", ("{'Ada': 'active', 'Can': 'inactive'}['Can']", "'inactive'")), [
  (W, "A dictionary is a collection of key and value pairs, written between braces. The glossary describes it as an associative array in which arbitrary keys are mapped to values, and the tutorial adds that, unlike sequences, which are indexed by a range of numbers, dictionaries are indexed by keys [[PSF]]."),
  (Y, "A dictionary answers the question what belongs to this key: the status of a user, the price of a product, the score of a player. The tutorial's example of changing a collection while looping uses a dictionary of users and their status, so the type is needed to follow the section on hazards."),
  (E, "The lookup users['Can'] gives 'inactive' for the dictionary {'Ada': 'active', 'Can': 'inactive'}. A loop over the dictionary visits its keys, so list(users) is ['Ada', 'Can'], and the items() method gives the pairs, so that for name, status in users.items() receives a key and a value in each iteration [[PSF]]."),
  (H, "The main operations are storing a value under a key and extracting the value given the key; a pair can be removed with del, so after del users['Can'] only Ada remains and len(users) is 1. Keys are unique, and iteration gives them in insertion order, as the tutorial's discussion of list(d) states [[PSF]]."),
  (K, "Asking for a key that does not exist raises a KeyError, here KeyError: 'Eda' for a user that is not in the dictionary. Keys must be hashable, which means that a key has a fixed value for its whole life so that Python can compute a number from it to find it again quickly, so a list, whose contents can change, cannot be used as a key and raises a TypeError, and a dictionary must not be resized while it is being looped over, as the section on hazards shows."),
 ]),
 ("LoopControl", None, 1, None, None, [
  (W, "Loop control is the set of statements and calls that change the course of a loop from the inside. A loop normally runs until its condition fails or its sequence is used up, but the program can also leave it early, skip a single iteration, or react to what happened when the loop ended. The statements break and continue belong here, and so do the call to sys.exit(), the else clause of a loop and the rules for the loop variable [[SW]]."),
  (Y, "Real programs rarely fit the pure pattern of a loop that runs to its test. A search should stop as soon as the item has been found, a login prompt should ignore one kind of input and react to another, and a program that was started by mistake should be stoppable. Loop control gives the author precise tools for each of these needs."),
  (H, "The branch has four groups. Early exit covers the ways of leaving a loop, skipping covers continue, loop completion explains what is true after a loop has ended, and the group on exceptions covers the signal mechanism that stands behind sys.exit(), Control-C and the clean-up clause finally."),
  (K, "Each tool changes the meaning of a loop, and a reader has to see all of them to know when a loop really ends. A loop of ten lines can have three exits, and a bug is often an exit that was forgotten or a skip that was placed before an important line."),
 ], None),
 ("EarlyExit", None, 2, "LoopControl", None, [
  (W, "An early exit leaves a loop before its condition fails or its sequence is exhausted. The chapter presents the break statement, the sys.exit() call and, as the way to stop a runaway program, the interrupt from the keyboard; the return statement, which leaves the function that holds the loop, completes the list [[SW]]."),
  (Y, "Early exits make loops fit the problem. A guessing game ends when the guess is right, not when the attempts are used up, and a menu ends when the user chooses to quit. Without them every such condition would have to be squeezed into the loop's own test."),
  (H, "The sections of the group are ordered by how far the exit reaches. A break leaves one loop, a return leaves a function, a call to sys.exit() leaves the program, and an interrupt from the keyboard stops the program from outside. Each reaches its target by a different mechanism, and each interacts differently with the else clause and with finally."),
 ], None),
 ("BreakStatement", None, 3, "EarlyExit", ("break", "break ends the innermost enclosing loop at once and skips the loop's else clause.", None), [
  (W, "A break statement ends the loop that contains it. In code it consists of the single keyword break, and when execution reaches it the program leaves the loop immediately [[SW]]. The reference documentation says that it terminates the nearest enclosing loop, skipping the optional else clause if the loop has one [[PSF]]."),
  (Y, "The break statement lets a loop run until a condition inside its block is met. This is the pattern of the book's second name program, which uses while True and breaks when the user has typed the right words, and of the Guess the Number program, which breaks out of the for loop when the guess is correct [[SW]]. Both could not be written as simply with the loop's own test."),
  (E, "The book uses break in yourName2.py, in swordfish.py, in the guessing game and in the player input loop of Rock, Paper, Scissors. The tutorial's search for prime numbers uses it to stop looking for factors as soon as the first one has been found [[PSF]]."),
  (H, "When break runs, the loop ends at once, the else clause of the loop is skipped, and the loop variable keeps the value it has: in a loop over range(10) that breaks when i is 3, the variable is still 3 afterwards [[PSF]]. Only the innermost loop is left, so a break inside the inner loop of two nested loops sends execution to the next iteration of the outer loop. When break passes out of a try statement that has a finally clause, the finally clause is executed first."),
  (K, "The statement can be used only inside a for or while loop, and not inside a function or class definition within that loop [[PSF]]; written anywhere else it is a SyntaxError that says 'break' outside loop, in agreement with the book's remark that Python will give you an error [[SW]]. A break also does not leave an outer loop, and a learner who wants to leave two loops at once needs another tool."),
 ]),
 ("ExitFunction", None, 3, "EarlyExit", ("sys.exit()", "sys.exit() raises SystemExit, which ends the program unless something intercepts it; finally clauses still run.", None), [
  (W, "The function sys.exit() ends a program before its last instruction. Programs always terminate when execution reaches the bottom of the instructions, but a call to sys.exit() terminates them earlier; because the function lives in the sys module, the module has to be imported first [[SW]]."),
  (Y, "A loop that is meant never to end by itself, such as a menu or a game, needs a deliberate way out. The book's exit example has an infinite loop with no break at all, and the only way the program ends is by the execution reaching the call to sys.exit(), which happens when the user types exit [[SW]]."),
  (E, "The call appears in the book's exitExample.py and in the quit command of Rock, Paper, Scissors. In scripts that report a failure it is also used with an argument: sys.exit('some error message') is a quick way to exit a program when an error occurs [[PSF]]."),
  (H, "The function raises a SystemExit exception, and the interpreter exits when that exception is not intercepted. The optional argument is the exit status: zero, the default, means success; any other integer means abnormal termination; any other object is printed to the error stream, the channel on which a program writes its error messages apart from its normal output, and gives the status 1 [[PSF]]. Since exit is an exception, the clean-up actions in finally clauses are honoured, and an outer part of the program can intercept the attempt. With sys.exit(3) inside a try block, a handler for SystemExit prints caught 3 and the program goes on."),
  (K, "The exit happens only when the call is made in the main thread and the exception is not intercepted [[PSF]]. SystemExit inherits from BaseException instead of Exception, so that a handler for Exception does not catch it by accident. And the import is required: calling sys.exit() without import sys raises a NameError."),
 ]),
 ("KeyboardInterruptStop", "Interrupting with Control-C", 3, "EarlyExit", ("Control-C", "Control-C raises KeyboardInterrupt in the running program, which stops it unless a handler catches the exception.", ("issubclass(KeyboardInterrupt, Exception)", "False")), [
  (W, "Pressing Control-C stops a program that is running. The book says that if a bug has caused an infinite loop, the key combination sends a KeyboardInterrupt error to the program and causes it to stop immediately; the same effect can be reached with the Stop button of the Mu editor [[SW]]. The documentation names the exception raised when the user hits the interrupt key, normally Control-C or Delete [[PSF]]."),
  (Y, "Every learner writes a runaway loop sooner or later. Knowing the key that stops it turns a frozen window into a small inconvenience, and it is the answer to the first practice question of the chapter. The book adds that Control-C is also handy to terminate a program immediately even when it is not stuck in an infinite loop [[SW]]."),
  (E, "The book's example is infiniteLoop.py, a while True loop that prints Hello, world! without end. In a terminal or in an editor's console, the same key stops a program that waits for input forever or computes for too long."),
  (H, "While a program runs, Python checks regularly whether an interrupt has been requested, and when it has, it raises KeyboardInterrupt in the running code [[PSF]]. If nothing handles the exception, the program stops and the error report ends with the line KeyboardInterrupt. A handler can catch it: a loop that raises it on purpose, inside try and except KeyboardInterrupt, prints stopped and goes on. The exception inherits from BaseException and not from Exception, so a handler that catches Exception does not prevent the interpreter from exiting [[PSF]]."),
  (K, "The documentation warns that catching KeyboardInterrupt requires special consideration: because it can be raised at unpredictable points, it may leave the running program in an inconsistent state, and it is generally best to allow it to end the program as quickly as possible [[PSF]]. The book calls it an error, while the documentation calls it an exception, and the section on exceptions explains the difference."),
 ]),
 ("ReturnFromLoop", "Return from a loop", 3, "EarlyExit", ("return inside a for loop", "A return statement leaves the function that contains it, and with it any loop that is running inside the function.", None), [
  (W, "A return statement ends a function and hands a value back to the place that called it, and a loop inside the function ends together with it. Chapter 1 showed how to call functions; writing your own is, in the book's words, the topic of the next chapter, so this section gives only what is needed to understand the effect on loops [[SW]]."),
  (Y, "Returning from inside a loop is the cleanest way to write a search: the function looks at each item and, as soon as one fits, returns it without any flag variable or extra test. The tutorial lists a return among the ways in which a loop can be left early [[PSF]]."),
  (E, "The shape appears in every function that looks for something in a collection, such as the first even number of a list or the first record that matches a name. The loop's else clause is not run when a return ends the loop, as the tutorial states [[PSF]]."),
  (H, "In the function first_even, a for loop looks at each item and returns the first one that is divisible by 2, and after the loop a second return gives None. Called with [1, 3, 4, 5], the function prints 4, because the loop is left at the third item; called with [1, 3], it prints None, because the loop ran to its end without a return."),
  (K, "The statement is allowed only inside a function; written at the top of a program it is a SyntaxError that says 'return' outside function. A return leaves the whole function, not just the loop, so any statement after the loop in that function is skipped as well."),
 ]),
 ("Skipping", None, 2, "LoopControl", None, [
  (W, "Skipping means giving up one iteration of a loop without giving up the loop. The continue statement is the tool: it ends the current pass through the block and starts the next one [[SW]]."),
  (Y, "A loop often meets items that need no processing, such as the wrong user name or an invalid entry. Skipping them with continue keeps the main work of the block at one level of indentation instead of burying it inside a long if statement."),
  (H, "The group has one section, on continue. Its meaning differs a little between the two loops: in a while loop execution returns to the test of the condition, and in a for loop it goes to the next item, a difference that matters when a counter is increased by hand."),
 ], None),
 ("ContinueStatement", None, 3, "Skipping", ("continue", "continue skips the rest of the block and goes back to test the condition, or to take the next item.", None), [
  (W, "A continue statement jumps back to the start of the loop and reevaluates the loop's condition. The book describes it as what happens when the program execution reaches a continue statement, and notes that this is also what happens when the execution reaches the end of the loop [[SW]]. The reference adds that in a for loop it continues with the next item [[PSF]]."),
  (Y, "The statement lets a loop discard an unwanted case early. The book's swordfish.py asks for a name and a password, and every name except Joe is sent back to the question with continue, so the password prompt appears only for Joe [[SW]]. Without it the rest of the block would have to sit inside an if."),
  (E, "The tutorial's example loops over the numbers from 2 to 9 and, for each even number, prints that it found an even number and continues, so that the odd-number message is printed only for the others [[PSF]]. Anywhere a loop has a precondition for its real work, a continue at the top of the block expresses it."),
  (H, "With the typed answers I'm fine, thanks. Who are you?, Joe, Mary, Joe and swordfish, swordfish.py asks Who are you? three times and the password question twice, and ends with Access granted. In a while loop the jump goes to the test of the condition, in a for loop to the next item, and when it passes out of a try statement with a finally clause, that clause runs first."),
  (K, "Like break, the statement is allowed only inside loops; anywhere else Python reports a SyntaxError, which the book also warns about [[SW]], and the message reads 'continue' not properly in loop. In a while loop a continue placed before the line that changes the counter creates an endless loop, because the test sees the same value again, while the equivalent for loop continues without trouble."),
 ]),
 ("LoopCompletion", None, 2, "LoopControl", None, [
  (W, "Loop completion is about what is true after a loop has ended: whether it ended by exhausting its supply or by a break, what value the loop variable has, and which of several possible endings occurred. The else clause of a loop and the lasting value of the loop variable are the two features of Python that make this visible [[PSF]]."),
  (Y, "Programs often need to know why a loop stopped. A search wants to say not found if it ran to the end, and the guessing game of the book decides between its success message and its failure message after the loop [[SW]]. Python offers a dedicated clause for the first purpose and leaves the loop variable in place for the second."),
  (H, "The group has three sections. The else clause runs when no break occurred, the section on the loop variable explains which value remains after the loop, and the section on the endings of a loop lists every way in which a loop can end and which of them runs the else clause."),
 ], None),
 ("LoopElseClause", None, 3, "LoopCompletion", ("for ... else:", "An else clause on a loop runs when the loop finishes without executing break.", None), [
  (W, "A loop can have an else clause, which runs when the loop finishes without executing break. In a for loop the clause is executed after the final iteration, and in a while loop after the condition becomes false; in either kind it is not executed if the loop was ended by a break [[PSF]]."),
  (Y, "The clause expresses a search that can fail in one place. Without it, a program needs a flag variable that is set before the loop, changed at the break and tested afterwards; with it, the failure case is written directly below the loop. The tutorial's own example looks for factors of numbers and reports a prime number when the loop falls through without finding one."),
  (E, "The tutorial prints, for the numbers 2 to 9, either an equation such as 4 equals 2 * 2 or the sentence 2 is a prime number, and it points out that the else clause belongs to the for loop and not to the if statement [[PSF]]. The feature is not part of the book's chapter and is an addition for the advanced course."),
  (H, "The prime-number loop prints 2 is a prime number, 3 is a prime number, 4 equals 2 * 2, 5 is a prime number, 6 equals 2 * 3, 7 is a prime number, 8 equals 2 * 4 and 9 equals 3 * 3. The clause also runs when the sequence is empty, since there is no break, and for a while loop it runs once the condition is false: a countdown from 3 reaches zero and then runs its else clause. A break skips it, and so do a return and an exception [[PSF]]."),
  (K, "The name misleads many readers. The tutorial suggests imagining the else paired with the if inside the loop, and notes that the clause has more in common with the else of a try statement, which runs when no exception occurs, than with the else of an if: the loop's else runs when no break occurs [[PSF]]. It does not mean that the loop condition failed unless nothing else ended the loop."),
 ]),
 ("LoopVariableScope", None, 3, "LoopCompletion", ("the variable after the loop", "The loop variable is overwritten on each pass and is not deleted when the loop ends; after a loop over an empty sequence it was never assigned.", None), [
  (W, "The loop variable of a for statement is an ordinary variable, and it lives on after the loop. The reference documentation states that the names in the target list are not deleted when the loop is finished, but if the sequence is empty they will not have been assigned to at all by the loop [[PSF]]."),
  (Y, "The fact is useful and dangerous at once. It lets the Guess the Number program read guesses_taken and guess after the loop to compose its final message [[SW]], and it lets a search report the item at which it stopped. It also means that a for loop can silently change a variable that the program had been using for something else."),
  (E, "After for i in range(5) has finished, printing i shows 4; after a loop that was ended by break at i equal to 3, printing i shows 3 [[PSF]]. In the Guess the Number program the variable guesses_taken keeps the number of the last attempt."),
  (H, "Each pass assigns the next item to the variable and overwrites everything assigned to it before, including assignments in the block: the documentation's loop sets i = 5 in the block, but the next pass replaces it, so all ten numbers from 0 to 9 are still printed [[PSF]]. If the loop runs over an empty sequence, the variable is never assigned, and reading it afterwards raises a NameError that says the name is not defined."),
  (K, "There is no separate scope for a loop. A variable named i that was set to a text before a loop that also uses i holds the last number after the loop and the text is lost. And a program that reads the loop variable after a loop that may be empty has to expect the NameError."),
 ]),
 ("LoopEnding", "Endings of a loop", 3, "LoopCompletion", ("five ways a loop can end", "A loop ends when its condition is false or its sequence is exhausted (both run the else clause), or when break, return or an unhandled exception leaves it (none run the else clause).", None), [
  (W, "A loop can end in several ways, and it matters which one happened. The first is that its condition becomes false, in a while loop, or that its iterator is exhausted, in a for loop. The others are a break statement, a return statement that leaves the function, and an exception that is not handled inside the loop, among which are the SystemExit raised by sys.exit() and the KeyboardInterrupt raised by Control-C [[PSF]]."),
  (Y, "The distinction decides what the program may assume afterwards. After a normal end the test failed or the data is used up; after a break the test may still be true and data may remain; after an exception the code that follows the loop is not reached at all. Reasoning correctly about the state after a loop needs this classification."),
  (E, "The reference documentation draws the line for the else clause: a loop's else clause runs when the condition becomes false or the iterator is exhausted, and does not run when the loop was terminated by a break; the tutorial adds that a return or a raised exception also skip the clause [[PSF]]."),
  (H, "A loop that breaks at the third pass of a loop whose limit is ten leaves its counter at 3, and the condition n < 10 is still true. A for loop with a break prints no message from its else clause, but it still runs the statement after the loop. A search function returns on the first hit and so never reaches its else clause or the code after the loop, and an unhandled exception leaves the loop at once."),
  (K, "A frequent assumption is that after a while loop its condition must be false. That holds only for a loop that ended normally; after a break the condition may well be true. The safe habit is to record the reason with the else clause, a flag or a return value, instead of inferring it from the state of the variables."),
 ]),
 ("ExceptionHandling", "Exceptions and warnings", 2, "LoopControl", None, [
  (W, "Exceptions and warnings are the signals through which Python reports that something has gone wrong or looks wrong. An exception interrupts the normal flow of the program; a warning reports a suspicious construct and lets the program go on. Three loop-related features of the chapter use these signals: sys.exit(), Control-C and the new warning about control flow in finally blocks [[PSF]]."),
  (Y, "Loops are where programs spend their time, and so they are where errors strike: a conversion of text typed by the user fails, a name is missing, a sequence is exhausted. Understanding the signal mechanism turns an error message from an alarming wall of text into a precise report, and it explains how a program can be stopped and cleaned up properly."),
  (H, "The group first defines the exception itself, then the finally clause that guarantees clean-up while an exception or a jump leaves a block, and finally the SyntaxWarning that Python 3.14 issues for a dangerous use of finally. The details of handling exceptions belong to a later chapter; the sections give what chapter 3 needs."),
 ], None),
 ("ExceptionSignal", "Exception", 3, "ExceptionHandling", ("10 * (1/0)", "An exception is an error detected during execution; unless a handler catches it, the program stops and prints the type of the exception and a message.", None), [
  (W, "An exception is an error that is detected while a program runs. The Python tutorial explains that even if a statement or expression is syntactically correct, it may cause an error when an attempt is made to execute it, and that errors detected during execution are called exceptions and are not unconditionally fatal [[PSF]]."),
  (Y, "Exceptions are the mechanism behind many things in this chapter: the ValueError of zip(strict=True), the StopIteration that ends a for loop, the SystemExit of sys.exit() and the KeyboardInterrupt of Control-C. A learner who knows how they travel understands why a loop can be left from the inside, and why code that catches too much can stop a program from ending."),
  (E, "Every program that fails shows one. The tutorial's first examples are 10 * (1/0), which raises a ZeroDivisionError with the message division by zero, a NameError for a missing name and a TypeError for adding a number to a string [[PSF]]. In loops, the typical sources are the conversion of typed text, the lookup of a missing key and the use of a variable that was never assigned."),
  (H, "When an exception is raised, the rest of the statement is abandoned and Python looks for a handler, searching outwards through the enclosing code. If none is found, the program stops with an error message whose last line gives the type and the details, preceded by a traceback of where the exception occurred [[PSF]]. A handler is written with try and except: a try block that converts 'x' with int() and an except ValueError block that prints bad number runs to the end and prints bad number."),
  (K, "Exceptions are organised in a family, and a handler matches the named type and the types derived from it. ValueError is derived from Exception, but SystemExit and KeyboardInterrupt are derived only from BaseException, so a handler for Exception does not catch them [[PSF]]. An unhandled exception inside a loop ends the loop and the program together, and the loop's else clause does not run."),
 ]),
 ("FinallyClause", None, 3, "ExceptionHandling", ("try: ... finally:", "A finally clause runs as the last task of a try statement, whether the block finished normally, raised an exception, or was left by break, continue, return or sys.exit().", None), [
  (W, "A finally clause is the part of a try statement that is intended to define clean-up actions that must be executed under all circumstances. The tutorial states that the clause executes as the last task before the try statement completes, and that it runs whether or not the try statement produces an exception [[PSF]]."),
  (Y, "Clean-up is what a program must do whatever happened: closing a file, releasing a connection, printing a closing message. The finally clause moves this duty out of the many places from which a block can be left and into one place."),
  (E, "The library documentation of sys.exit() says that cleanup actions specified by finally clauses of try statements are honored when the program exits [[PSF]]. The tutorial's example raises a KeyboardInterrupt inside a try block and shows the message Goodbye, world! printed by the finally clause before the error report appears."),
  (H, "If an exception occurs in the try block and is not handled, it is saved, the finally clause is executed, and the exception is raised again at the end of the clause. If the try block reaches a break, continue or return statement, the clause is executed just before the statement takes effect [[PSF]]. In a loop that breaks at i equal to 1 from inside a try block, the clause prints cleanup 0 and then cleanup 1, so it ran on the way out of the loop as well as on the normal pass. Likewise, int('x') in a try block with only a finally clause prints cleanup and then still raises the ValueError."),
  (K, "A break, continue or return statement inside the finally clause itself discards the saved exception and lets the program continue as if nothing had happened; the tutorial calls this confusing and discouraged, and since Python 3.14 the compiler warns about it [[PSF]]. The next hazard in the chapter, leaving a finally block, describes it."),
 ]),
 ("SyntaxWarning", None, 3, "ExceptionHandling", ("SyntaxWarning: 'break' in a 'finally' block", "A SyntaxWarning is reported while the code is compiled when it is legal but probably wrong; it does not stop the program.", None), [
  (W, "A SyntaxWarning is a message issued by the compiler for code that is legal but probably a mistake. Unlike a SyntaxError, it does not prevent the program from running. Python 3.14 uses it for one new case: the compiler now emits a SyntaxWarning when a return, break or continue statement has the effect of leaving a finally block [[PSF]]."),
  (Y, "A warning lets the language point to a problem without breaking programs that already exist. PEP 765 gives its reason: the semantics of leaving a finally block are surprising for many developers, and a swallowed exception, one that is discarded without any report, is more likely to slip through testing than an incorrect return value [[P765]]."),
  (E, "The message appears on the error stream when a program or module containing the construct is compiled. The PEP expects it to be seen by the project maintainer when static analysis (a tool that examines code without running it) or continuous integration (a server that rebuilds and tests a project after every change) compiles the code, while end users see it only if they skip precompilation, the step that compiles a package's files when it is installed [[P765]]. The What's New document says that the filter ignore::SyntaxWarning turns all syntax warnings off [[PSF]]."),
  (H, "A program that leaves a finally block with break still runs to its end: under Python 3.14 it prints its output and the error stream shows SyntaxWarning: 'break' in a 'finally' block, while under Python 3.12 nothing is reported, because the check does not exist there. Compiling the same code while recording warnings finds exactly one warning under 3.14 and none under 3.12."),
  (K, "The word warning invites ignoring it, but this one points to code that really loses exceptions. The PEP also warns about strictness: code run with -We, which turns warnings into errors, may stop working once the warning is introduced [[P765]]. A program that must run on several versions of Python must expect the warning on some of them and not on others."),
 ]),
 ("Module", None, 1, None, None, [
  (W, "A module is a unit of Python code that a program can load and use, and this branch of the chapter explains how to do so. The book introduces the idea in one passage: Python comes with a set of modules called the standard library, and each module is a Python program that contains a related group of functions that can be embedded in your programs [[SW]]. Python's glossary gives the formal version, an object that serves as an organizational unit of Python code and has a namespace containing arbitrary Python objects [[PSF]]."),
  (Y, "The built-in functions that every program can call, such as print, input and len, are not enough for real work. Modules give a program access to mathematics, random numbers, the operating system and the interpreter itself, without making every program carry that code, and they keep the names of each part of the code apart from the names of the others."),
  (H, "The branch has three groups. The import forms are the ways of writing the statement that loads a module, the module basics explain what a module is, how Python finds it and what goes wrong when two modules share a name, and the standard modules random and sys are the two that the chapter uses."),
  (K, "Most trouble with modules comes from names: an import that brings in more names than the author expected, a file that has the name of a module and hides it, or a prefix that was forgotten. The sections point out each case."),
 ], None),
 ("ImportForm", None, 2, "Module", None, [
  (W, "An import form is one of the ways of writing an import statement. The chapter shows three: the plain import of one module, the import of several modules in one statement, and the star import; the from form, which names the wanted names, completes the picture [[SW]]."),
  (Y, "The forms differ in where the imported names end up and how much of the module they bring. A plain import keeps the module's names under the module's name, the from form brings in only the names listed, and the star form brings in every public name, and the difference decides how readable and how safe the program is."),
  (H, "All forms perform the same two steps, which the reference documentation describes: first the module is found, and loaded and initialized if necessary; then a name or names are defined in the current namespace, just as an assignment statement would define them [[PSF]]. They differ in the second step."),
 ], None),
 ("ImportStatement", None, 3, "ImportForm", ("import random", "import makes a module's names available under the module's name, as random.randint(1, 10).", None), [
  (W, "The import statement loads a module and makes it available to the program. The book says that before the functions of a module can be used, the module must be imported, and that an import statement consists of the import keyword, the name of the module and, optionally, more module names separated by commas [[SW]]."),
  (Y, "The standard library holds far more functions than the language could carry as built-ins. Importing only the modules a program needs keeps the program's own names clear and makes the origin of each function visible at the place where it is used."),
  (E, "The first import in the chapter is import random, which gives access to random.randint(). The Guess the Number program imports random, the exit example imports sys, and the Rock, Paper, Scissors program imports both [[SW]]."),
  (H, "The reference documentation divides the work into two steps: find the module, loading and initializing it if necessary, and then bind a name in the current namespace [[PSF]]. After import random, the name random refers to the module and its function is called as random.randint(1, 10), which evaluates to a random integer between the two numbers. Five such calls in a loop print five integers between 1 and 10, and with random.seed(3) they are 4, 10, 9, 3 and 6 in both Python 3.12 and Python 3.14. Each module is loaded only once per interpreter session, the statements that initialize it being executed the first time the name is imported [[PSF]]."),
  (K, "Forgetting the import is the usual error: calling random.randint(1, 10) without it raises a NameError, because the name random does not exist. Asking for a module that cannot be found raises a ModuleNotFoundError that says No module named, followed by the name [[PSF]]."),
 ]),
 ("MultipleImport", None, 3, "ImportForm", ("import random, sys, os, math", "One import statement can name several modules separated by commas.", None), [
  (W, "A single import statement can name several modules, separated by commas. The book's example imports four of them at once: import random, sys, os, math [[SW]]. The reference documentation says that the two steps are then carried out separately for each clause, just as though the clauses had been separated out into individual import statements [[PSF]]."),
  (Y, "The form is shorter than four separate lines, and the book uses it in the first line of the Rock, Paper, Scissors program, import random, sys, because the program needs both modules. It is a matter of style and not of meaning, which is why a style guide has an opinion about it."),
  (E, "The form is common in the first lines of short scripts. The book says that after such a statement any function of the four modules can be used, and that more about them follows later in the book [[SW]]."),
  (H, "Each module in the list is imported and bound to its own name. After import random, sys, os, math, the names random, sys, os and math all refer to modules, and printing the __name__ of each gives random sys os math. The behaviour is the same as for four statements, one after the other."),
  (K, "PEP 8, the style guide for Python code, says that imports should usually be on separate lines and gives import sys, os as wrong, while from subprocess import Popen, PIPE, which takes several names from one module, is fine [[PEP8]]. Separate lines make it easier to add or remove a module and to see the change in a version-control diff."),
 ]),
 ("StarImport", None, 3, "ImportForm", ("from random import *", "from module import * brings every public name into the program without the module prefix.", None), [
  (W, "The star import brings all the public names of a module into the program, so that they can be used without the module's name in front. The book writes it as the from keyword, the module name, the import keyword and a star, as in from random import *, and says that calls to the functions in random then no longer need the random. prefix [[SW]]."),
  (Y, "Its attraction is less typing. The tutorial agrees that it is acceptable to save typing in interactive sessions but says that in general the practice of importing * from a module is frowned upon, since it often causes poorly readable code and introduces an unknown set of names that may hide things already defined [[PSF]]."),
  (E, "The book mentions the form only to recommend against it: using the full name makes for more readable code, so the import random form is better [[SW]]. PEP 8 uses the name wildcard import for the star form and states that wildcard imports should be avoided, because they make it unclear which names are present in the namespace, and names one defensible use, republishing an internal interface as part of a public API [[PEP8]]."),
  (H, "The reference documentation says that all public names defined in the module are bound in the local namespace. The public names are those listed in the module's __all__ variable if it exists, and otherwise every name that does not begin with an underscore [[PSF]]. The random module lists 26 names in __all__ in both Python 3.12 and Python 3.14. The form is allowed only at the top level of a module, that is, in a statement that is not inside a function or class; inside a function it raises a SyntaxError that says import * only allowed at module level."),
  (K, "The danger is silent replacement. Before from math import * the call pow(2, 3) gives 8, the result of the built-in function; afterwards it gives 8.0, because the pow of the math module has replaced the built-in one without any message. The reader of the program has no way to see which names arrived, which is the reason for the advice in the book and in PEP 8."),
 ]),
 ("FromImport", "From import", 3, "ImportForm", ("from math import sqrt", "from module import name binds only the listed names, which are then used without the module prefix; as gives a different name.", None), [
  (W, "The from form of the import statement imports chosen names of a module directly into the program. After from math import sqrt, the function is called as sqrt(16), without the prefix math. The tutorial notes that this variant does not introduce the module name itself into the local namespace [[PSF]]. A name can also be bound under another name with as, as in import math as m."),
  (Y, "The form sits between the plain import and the star import. It keeps the names short, as the star form does, but it lists them explicitly, so the reader can see which names come from where and no unknown names arrive. PEP 8 accepts it for several names from one module and recommends absolute forms of import [[PEP8]]."),
  (E, "The chapter shows the from form only with a star, but the Python code that students will read uses the form with listed names constantly. PEP 8 gives from subprocess import Popen, PIPE as a correct example, and the tutorial's examples import fib and fib2 from a module named fibo [[PEP8]] [[PSF]]."),
  (H, "The reference documentation describes the process: the module is found and loaded, then for each listed name the module is checked for an attribute of that name, and a reference to the value is stored in the current namespace, under the name in the as clause if there is one [[PSF]]. After from math import sqrt, sqrt(16) gives 4.0 while the name math does not exist and raises a NameError; after import math as m, m.sqrt(25) gives 5.0 and m.__name__ is still math."),
  (K, "If the module has no attribute of the requested name, Python raises an ImportError that says cannot import name followed by the name and the module. And a name imported in this way can replace a name the program already had, just as a star import can, but only the names that are listed."),
 ]),
 ("ModuleBasics", "Module basics", 2, "Module", None, [
  (W, "The module basics are the facts about modules that every import relies on: that a module is a file with its own namespace, that Python comes with a standard library of ready-made modules, that names inside a module are reached with a dotted name, that Python searches a list of places to find a module, and that a file with the wrong name can hide a real module."),
  (Y, "A learner who knows these facts can predict what an import will do and can diagnose its failures. The same facts are needed for every later chapter, because every library that the course uses arrives as a module."),
  (H, "The group goes from the object to the problems that surround it. The module file is defined first, then the standard library, the namespace of a module and the search path, and finally the hazard that the book singles out in a box of its own, the overwriting of module names [[SW]]."),
 ], None),
 ("ModuleFile", "Module file", 3, "ModuleBasics", ("math.__name__", "A module is a file of Python definitions and statements; importing it creates a module object that carries its own name and namespace.", None), [
  (W, "A module is a file that contains Python definitions and statements. The tutorial states that the file name is the module name with the suffix .py appended, and that within a module the module's name is available as the value of the global variable __name__ [[PSF]]. The glossary adds that modules are loaded into Python by the process of importing."),
  (Y, "Modules let code be written once and used by many programs, and they split a large program into files that can be understood one at a time. The book's standard library is a collection of such files, each holding a related group of functions [[SW]]."),
  (E, "The random module of the standard library is a file named random.py, a fact that the book's warning about file names depends on [[SW]]. A program of your own that is saved in the same folder can import another file of yours in the same way."),
  (H, "Importing a module creates a module object. Its type is module, its __name__ is the name it was imported under, so math.__name__ is 'math', and its attributes are the names defined in the file. A module may contain executable statements; these initialize it and are run only the first time it is imported [[PSF]]. When a file is run directly as the program, its __name__ is '__main__'."),
  (K, "A module is an object that exists in the running program, not merely a file on disk, and importing it twice does not run it twice. Changing the file while the interpreter is running does not change the module that is already loaded."),
 ]),
 ("StandardLibrary", "Standard library", 3, "ModuleBasics", ("import math", "The standard library is the set of modules that come with Python; the built-in functions need no import, the modules do.", None), [
  (W, "The standard library is the set of modules that Python comes with. The book distinguishes it from the built-in functions: all Python programs can call a basic set of built-in functions, including print(), input() and len(), while the modules of the standard library each have to be imported [[SW]]. The tutorial calls it a library of standard modules, described in the Library Reference [[PSF]]."),
  (Y, "The library saves the effort of writing common code. The book names four of its modules: math, with mathematics-related functions, random, with functions related to random numbers, and sys and os, which it says will be explained later [[SW]]. Because the library is installed with Python, a program that uses it works on every machine that has the interpreter."),
  (E, "The two modules of this chapter are random and sys. The tutorial points out that some modules are built into the interpreter and that sys is built into every Python interpreter [[PSF]]. Programs that need more than the library offers use packages from outside, which chapter 1 introduced."),
  (H, "A built-in function is available at once: len('hello') is 5 in a fresh program. A module is not: math.sqrt(16) in a fresh program raises a NameError that says name 'math' is not defined, and after import math the same call gives 4.0. The function's name is looked up inside the module, which the next sections describe."),
  (K, "Built-in names are not protected. The book lists the names that people often take for their own variables and files, among them all, any, list, max, min, open, set, str, sum and type, and advises against it [[SW]]. A program that assigns to such a name hides the function for as long as the assignment stands."),
 ]),
 ("ModuleNamespace", "Module namespace", 3, "ModuleBasics", ("math.sqrt(16)", "Every module keeps its names in its own namespace; a dotted name such as random.randint reaches into it.", None), [
  (W, "A namespace is the place where a variable is stored, and every module has its own. The glossary says that namespaces support modularity by preventing naming conflicts, and that they aid readability by making it clear which module implements a function: writing random.seed() or itertools.islice() makes clear that those functions are implemented by the random and itertools modules [[PSF]]."),
  (Y, "Separate namespaces allow two modules to use the same name for different things without harm, and they let the author of a module use global variables without worrying about accidental clashes with the user's names [[PSF]]. For the reader of a program the dotted name is documentation: it says where the function comes from."),
  (E, "The book explains the dotted name for random.randint(): because randint() is in the random module, random. has to be entered in front of the function name to tell Python to look for the function inside the module [[SW]]. The same pattern is sys.exit(). In the glossary's terms, the part after the dot is an attribute of the module."),
  (H, "After import math the name math refers to the module object, and math.sqrt looks up sqrt in the module's own namespace, so math.sqrt(16) evaluates to 4.0. The function dir lists the names of a module, and 'sqrt' is among the names of math [[PSF]]."),
  (K, "A name that the module does not have raises an AttributeError, and the message names both the module and the attribute: module 'math' has no attribute 'nope'. A mistyped function name therefore gives this error, whereas a forgotten prefix gives a NameError, and telling them apart points to the cause."),
 ]),
 ("ModuleSearchPath", "Module search path", 3, "ModuleBasics", ("sys.path", "Python looks for an imported module first in a cache of loaded modules and among the built-in modules, then in the directories listed in sys.path, beginning with the script's directory.", None), [
  (W, "The module search path is the list of places in which Python looks for a module that has been imported. The tutorial explains that for a module named spam the interpreter first searches for a built-in module with that name, and if none is found it searches for a file named spam.py in the directories given by the variable sys.path [[PSF]]."),
  (Y, "The search path explains why an import works in one folder and fails in another, and why a file that you saved yourself can replace a library module. It is the background of the book's warning not to give your programs the names of Python's modules [[SW]]."),
  (E, "The tutorial says that sys.path is initialized from the directory containing the input script, or the current directory when no file is specified, from PYTHONPATH, and from an installation-dependent default [[PSF]]. When Python runs code given with the -c option, the first entry is the empty string, which means the current working directory."),
  (H, "Before it searches at all, the import system looks in sys.modules, a mapping that serves as a cache of all modules previously imported; a module found there is used at once [[PSF]]. Before import math the name 'math' is not in sys.modules in a fresh program, and afterwards it is. The directory of the running script is placed at the beginning of the search path, ahead of the standard library path, so scripts in that directory are loaded instead of modules of the same name [[PSF]]."),
  (K, "Because each module is imported only once per interpreter session, a change in a module's file is not noticed until the interpreter is restarted, or the module is reloaded with importlib.reload() [[PSF]]. A program may add to sys.path, but the documentation warns that the entry prepended at start-up is a potentially unsafe path [[PSF]]."),
 ]),
 ("ModuleNameClash", "Overwriting a module name", 3, "ModuleBasics", ("a script saved as random.py", "A file or variable that has the name of a Python module or built-in function hides the real one and produces confusing errors.", None), [
  (W, "A file that has the name of a module hides that module. The book gives the warning in a box of its own: when you save your Python scripts, take care not to give them a name that is used by one of Python's modules, such as random.py, sys.py, os.py or math.py [[SW]]. The same applies to the names of built-in functions used as variable names."),
  (Y, "The mistake is hard to find because the code looks correct. A program that says import random and calls random.randint() is right, and it fails only because a file called random.py sits next to it. Knowing the cause saves a learner hours of searching in the wrong place."),
  (E, "The book describes the situation: if you accidentally name one of your programs random.py and use an import random statement in another program, your program will import your random.py file instead of Python's random module [[SW]]. A folder of exercises in which each file is named after its topic invites exactly this collision."),
  (H, "The reason is the search path: the script's directory comes first, ahead of the standard library, so the local file is found before the real module [[PSF]]. In a folder that holds a random.py with the single line x = 1 and a program that imports random and calls random.randint(1, 10), Python stops with AttributeError: module 'random' has no attribute 'randint', the error the book names. Python 3.14 adds a hint to the message that suggests renaming the file, since it has the same name as the standard library module. Assigning a list to the name list likewise makes list('abc') fail with a TypeError."),
  (K, "The fix is to rename the file, and the lesson is to choose names that are not taken. The book's list of common Python names to avoid includes all, any, date, email, file, format, hash, id, input, list, min, max, object, open, random, set, str, sum, test and type [[SW]]."),
 ]),
 ("StandardModule", "Standard modules in the chapter", 2, "Module", None, [
  (W, "The two standard modules of the chapter are random, which supplies the random numbers of the two games, and sys, which supplies sys.exit() and gives access to the interpreter. Both are imported with an ordinary import statement and used through dotted names [[SW]]."),
  (Y, "They show what a module is for: random answers the question of how a program can behave unpredictably, and sys answers the question of how a program can talk to the interpreter that runs it. Both are used again in later chapters."),
  (H, "The sections below take each module in turn, saying what the names used in the chapter do and which cautions the documentation attaches to them."),
 ], None),
 ("RandomModule", "Random module", 3, "StandardModule", ("random.randint(1, 20)", "random.randint(a, b) returns a pseudo-random integer N with a <= N <= b, both ends included.", None), [
  (W, "The random module provides functions that generate pseudo-random numbers, and the chapter uses one of them, random.randint(). The library documentation defines it: random.randint(a, b) returns a random integer N such that a <= N <= b, and it is an alias for randrange(a, b+1) [[PSF]]. The book says that the call evaluates to a random integer value between the two integers that you pass it [[SW]]."),
  (Y, "Games, simulations and tests all need a source of chance. Guess the Number draws its secret with random.randint(1, 20), and Rock, Paper, Scissors draws the computer's move with random.randint(1, 3) [[SW]]."),
  (E, "Besides randint the module offers functions for sequences, for real numbers and for several distributions. The library documentation names the Mersenne Twister as the core generator and notes that, being completely deterministic, it is not suitable for all purposes [[PSF]]."),
  (H, "Both ends are included, which is the opposite of range. In 200 draws from random.randint(1, 3) after random.seed(1) all of 1, 2 and 3 appear, whereas 200 draws from random.randrange(1, 3) give only 1 and 2. The numbers are pseudo-random, produced by a deterministic algorithm, so seeding with the same value gives the same sequence again: after random.seed(7), the first five numbers from randint(1, 20) are repeated exactly by a second seeding with 7 [[PSF]]."),
  (K, "The documentation warns that the pseudo-random generators of this module should not be used for security purposes and points to the secrets module for those uses [[PSF]]. A second caution is the off-by-one between randint and range: randint(1, 10) can return 10, whereas an index chosen from range(10) never reaches 10."),
 ]),
 ("SysModule", "Sys module", 3, "StandardModule", ("sys.exit()", "The sys module gives a program access to the interpreter: sys.exit() ends it, sys.path lists the module search directories and sys.modules holds the modules already loaded.", None), [
  (W, "The sys module gives a program access to the interpreter that runs it. The tutorial singles it out as one particular module that deserves attention, and states that it is built into every Python interpreter [[PSF]]. The book imports it for one function, sys.exit(), which ends the program [[SW]]."),
  (Y, "A program sometimes has to act on the interpreter and not on its own data: to stop, to report an exit status, to see where modules are searched for. The sys module is the place where such facilities are found, and the chapter's use of it is the first of many."),
  (E, "Three of its names matter in this chapter. sys.exit() ends the program with a status, sys.path is the list of directories searched for modules, and sys.modules is the mapping of modules that have already been loaded [[PSF]]."),
  (H, "A program has to import sys before it uses it. The library documentation describes sys.path as a list of strings that specifies the search path for modules, which a program is free to modify for its own purposes [[PSF]], and sys.modules as a dictionary that maps module names to modules that have already been loaded. After import math the key 'math' is present in it."),
  (K, "Modifying sys.path or sys.modules is a way of changing how Python itself behaves. The documentation notes that deleting essential items from sys.modules may cause Python to fail, and that a potentially unsafe path is prepended to sys.path at start-up [[PSF]]. For the purposes of this chapter, reading these names is enough."),
 ]),
 ("ModernPractice", None, 1, None, None, [
  (W, "Modern practice is what current Python and its community add to the chapter of the book. The book teaches loops and imports as they are needed by a beginner; an advanced course also has to know the idioms that Python has gained since, the habits that the official style guide asks for, and the places where the language itself now warns about dangerous code [[PSF]]."),
  (Y, "A programmer who learns only the book's forms writes code that works but reads as dated, and one who has not seen the hazards writes loops that fail only on some data. The sources of this branch are the Python tutorial and reference, the style guide PEP 8 and three PEPs, so each point can be traced to a document that anyone can read."),
  (H, "The branch has two groups. Expression style covers the assignment expression that lets a loop read and test in one line and the import habits of PEP 8; the hazards are two constructs that look harmless and are not, namely changing a collection while looping over it and leaving a finally block."),
  (K, "Newer is not automatically better. The assignment expression is worth using when it shortens and clarifies a loop, and not when it makes a line harder to read, and the style guide itself says that its rules are guidelines for readable code."),
 ], None),
 ("ExpressionStyle", "Expression style", 2, "ModernPractice", None, [
  (W, "Expression style is the way in which the same behaviour can be written more clearly. Two points belong to it in this chapter: the assignment expression, which lets a loop read a value and test it in a single line, and the import conventions of PEP 8, which fix where and how imports are written [[P572]] [[PEP8]]."),
  (Y, "Clear code is read many more times than it is written. The assignment expression removes a repeated line from a common loop pattern, and the import conventions make the dependencies of a file visible at a glance, so both help the next reader."),
  (H, "The first section shows a loop in its older and newer forms, executed side by side; the second lists the rules of PEP 8 and sets them against the habits of the book."),
 ], None),
 ("AssignmentExpressionLoop", None, 3, "ExpressionStyle", ("while chunk := file.read(8192):", "An assignment expression names a value inside a condition, so a loop can read and test in one line.", None), [
  (W, "An assignment expression gives a name to a value inside an expression, and it is written NAME := expression. PEP 572 defines it: the value of the expression is the same as the value of the incorporated expression, with the additional side effect that the target is assigned that value; the operator became informally known as the walrus operator [[P572]]."),
  (Y, "The PEP's rationale is that naming the result of an expression is an important part of programming, and that until then it was possible only in statement form [[P572]]. In a loop the difference is concrete: without the new form the value must be read once before the loop and again at the end of the block, or the loop must be written as while True with a test and a break."),
  (E, "The PEP lists the loop while chunk := file.read(8192): process(chunk) as an example of a loop that cannot be trivially rewritten using the two-argument form of iter() [[P572]]. The tutorial remarks that in Python, unlike C, assignment inside expressions must be done explicitly with the walrus operator, which avoids typing = in an expression when == was intended [[PSF]]."),
  (H, "The call file.read(n) reads at most n characters and returns an empty string when the end of the file has been reached [[PSF]]. Because the empty string counts as false, the loop ends at the end of the data. With file = io.StringIO('abcdefgh'), an in-memory text stream that is read like a file, the loop while chunk := file.read(3): print(chunk) prints abc, def and gh, which is exactly what the longer version with while True, an assignment, an if not chunk test and a break prints. In a larger expression the form needs parentheses: (n := 5) + 1 is 6."),
  (K, "The PEP prohibits unparenthesized assignment expressions at the top level of an expression statement, so y := 5 on its own line is a SyntaxError [[P572]]. The feature was added in Python 3.8, so it does not run on older interpreters, and a line that tries to do too much with it is harder to read than the two lines it replaces."),
 ]),
 ("ImportStyle", None, 3, "ExpressionStyle", ("import os on one line, import sys on the next", "PEP 8 advises one import per line and against wildcard imports.", None), [
  (W, "PEP 8, the style guide for Python code, has a section on imports. It says that imports should usually be on separate lines, that they are always put at the top of the file, just after any module comments and docstrings (the string at the start of a module or function that documents it) and before module globals and constants, and that wildcard imports should be avoided [[PEP8]]."),
  (Y, "Habits of this kind make programs predictable. If every file starts with its imports, a reader sees at once what the file depends on, and if every import is a line of its own, a change to the list of dependencies is a change to a single line."),
  (E, "The book's Rock, Paper, Scissors program begins with import random, sys, which PEP 8 would write as two lines. The guide gives import os and import sys as correct and import sys, os as wrong, while from subprocess import Popen, PIPE is acceptable [[PEP8]]."),
  (H, "The guide asks for imports in three groups, in this order: standard library imports, related third-party imports, and local application or library imports, with a blank line between each group. It recommends absolute imports as more readable, and accepts explicit relative imports for complex package layouts [[PEP8]]."),
  (K, "These are rules of style and not of the language: the book's one-line import works. The guide describes its own recommendations as conventions for readable code, so a project may agree on others. The rule against the star import is the one with a practical consequence, since the form can hide the origin of names and replace existing ones."),
 ]),
 ("Hazard", None, 2, "ModernPractice", None, [
  (W, "A hazard is a construct that looks harmless but makes a program behave wrongly, often without any error message. Two loop-related hazards are documented in the official sources the chapter draws on: changing a collection while looping over it, and leaving a finally block with a control-flow statement [[PSF]]."),
  (Y, "Hazards are costly because their effects are quiet. A loop that skips items or a program that swallows an exception can pass its first tests and fail later with real data, and the cause is far from the symptom."),
  (H, "For each hazard the sections give the documented advice and show the wrong behaviour next to the safe one, using programs that were run so that the effects described are real."),
  (K, "The two hazards share a pattern: the unsafe form needs one line less and works on the first test. The safe forms, looping over a copy or building a new collection, and letting an exception propagate instead of jumping out of a finally block, cost a line or two more, and a reader who knows the hazard sees at once why they are written that way."),
 ], None),
 ("MutationWhileIterating", None, 3, "Hazard", ("for user in users: del users[user]", "Changing a collection while iterating over it is tricky to get right; loop over a copy or build a new collection.", None), [
  (W, "Changing a collection while a loop is walking through it is tricky to get right. The tutorial says so in its section on the for statement: code that modifies a collection while iterating over that same collection can be tricky, and it is usually more straightforward to loop over a copy of the collection or to create a new collection [[PSF]]."),
  (Y, "The danger is that the loop and the change disturb each other. The iterator keeps a position in the collection, and an item that is added or removed moves the positions of the others, so the loop may skip items, visit items twice or stop with an error. The tutorial's looping techniques repeat the advice: it is often simpler and safer to create a new list instead [[PSF]]."),
  (E, "The tutorial's example is a dictionary of users and their status from which the inactive users must be removed; it shows the two safe strategies, iterating over users.copy().items() and building a new dictionary of the active users [[PSF]]. The same task appears whenever records are filtered in place."),
  (H, "Deleting from a dictionary while looping over it fails at once: for each user in users, del users[user] raises RuntimeError: dictionary changed size during iteration. Over a list the effect is silent: removing each 2 from [1, 2, 2, 3] while looping leaves [1, 2, 3], since the second 2 moves into the position the loop has already passed. Looping over a copy removes the inactive users and leaves {'Ada': 'active'}, and building a new list with a test gives [1, 3]."),
  (K, "The silent case is the dangerous one, because no exception warns of the mistake. The rule is simple: whatever you loop over, do not add or remove items of it in the loop block; either collect what you want in a new collection, or loop over a copy and change the original."),
 ]),
 ("FinallyExit", None, 3, "Hazard", ("break inside a finally block", "Python 3.14 emits a SyntaxWarning when return, break or continue leaves a finally block.", None), [
  (W, "Leaving a finally block with a return, break or continue statement discards the exception that was on its way. The reference documentation states that if the finally clause executes one of these statements, the saved exception is discarded, and its example is a function that divides by zero in a try block and returns 42 from the finally clause, so that the function returns 42 and no exception is seen [[PSF]]."),
  (Y, "PEP 765 explains why the behaviour is a problem: the semantics are surprising for many developers, and a swallowed exception, one that is discarded without any report, is more likely to slip through testing than an incorrect return value [[P765]]. PEP 8 had already advised against such statements, because they implicitly cancel any active exception that is propagating through the finally suite [[PEP8]]."),
  (E, "The PEP's analysis of real code found that the pattern is rare, at 2 per million lines of code in the top 8,000 packages of PyPI, the Python Package Index from which pip installs packages, and that most of its uses were incorrect and introduced unintended exception-swallowing bugs [[P765]]. In Python 3.14 the compiler emits a SyntaxWarning when a return, break or continue statement has the effect of leaving a finally block [[PSF]]."),
  (H, "In a loop whose try block raises a ValueError and whose finally block breaks, the break ends the loop, the ValueError is discarded and the program goes on to print done, with no sign of the error. Python 3.14 reports SyntaxWarning: 'break' in a 'finally' block when such code is compiled, while Python 3.12 is silent. The warning is not given when the jump stays inside the block, for instance for a loop that is itself inside the finally block, or for a function defined in it [[P765]]."),
  (K, "The behaviour is unchanged; only the warning is new, and it is a warning and not an error. The PEP leaves open whether it will ever become a SyntaxError and warns that code run with -We may stop working [[P765]]. The remedy is to restructure: let the exception propagate, or put the break or return after the whole try statement."),
 ]),
]

# ---- citation markers become author-year strings; the io examples become checks ----
NODES = [n[:5] + ([(f, __import__("re").sub(r"\[\[[A-Z0-9]+\]\]", lambda m: CITES[m.group(0)], t)) for f, t in n[5]],) + n[6:] for n in NODES]
assert not any("[[" in t for n in NODES for f, t in n[5]), "unexpanded citation marker"

# claims whose output is quoted in the texts above: (expression, expected repr). The helpers run(), rc(), err(), msg(), stuck(), warnline(),
# clash() and pathfirst() are defined by PRELUDE below and execute the programs of PG in a separate interpreter process.
_L = lambda *xs: "".join(x + "\n" for x in xs)
CHECKS = [
 # loop basics and while
 ("run('if')", repr("Hello, world.\n")), ("run('while')", repr("Hello, world.\n" * 5)), ("stuck('while_stuck')", "True"), ("stuck('while_true_stuck')", "True"),
 ("run('while_count')", repr("5\n")), ("run('while_false')", repr("done\n")), ("run('last_i')", repr("4\n")),
 ("[bool(0), bool(0.0), bool(''), bool('x')]", "[False, False, False, True]"), ("run('while_not', '\\nabc\\n')", repr(">>'abc'\n")),
 ("run('yourname', 'x\\nyour name\\n') == run('yourname2', 'x\\nyour name\\n')", "True"), ("run('break3')", repr("3\n")),
 ("run('swordfish', 'Ann\\nJoe\\nswordfish\\n').count('What is the password?')", "1"), ("run('swordfish', 'Ann\\nBob\\n').count('What is the password?')", "0"),
 ("run('five_for') == run('five_while')", "True"), ("run('five_for').splitlines()[0]", repr("Hello!")), ("run('five_for').splitlines()[-1]", repr("Goodbye!")),
 ("len(run('five_for').splitlines())", "7"), ("run('five_for').splitlines()[1]", repr("On this iteration, i is set to 0")),
 ("stuck('while_continue_stuck')", "True"), ("run('for_continue')", repr("4\n")),
 # accumulator
 ("run('gauss')", repr("5050\n")), ("run('gauss_reset')", repr("100\n")), ("len(range(101))", "101"), ("50 * 101", "5050"), ("sum(range(100))", "4950"),
 ("err('gauss_noinit')", repr("NameError: name 'total' is not defined")),
 # nesting
 ("run('nested_count')", repr("12\n")), ("run('nested_break')", repr("0 0\n1 0\n")), ("1000 * 1000", "1000000"),
 # Guess the Number and Rock, Paper, Scissors
 ("'Good job! You got it in 4 guesses!' in run('guess16', '10\\n15\\n17\\n16\\n')", "True"),
 ("'Nope. The number was 16\\n' in run('guess16', '1\\n2\\n3\\n4\\n5\\n6\\n')", "True"), ("run('guess16', '1\\n2\\n3\\n4\\n5\\n6\\n').count('Your guess is too low.')", "6"),
 ("run('guess16', '1\\n2\\n3\\n4\\n5\\n6\\n').count('Take a guess.')", "6"), ("err('guess16', 'abc\\n').split(':')[0]", repr("ValueError")),
 ("'PAPER versus...\\nPAPER\\nIt is a tie!' in run('rps_paper', 'p\\nq\\n')", "True"), ("'0 Wins, 0 Losses, 1 Ties' in run('rps_paper', 'p\\nq\\n')", "True"),
 ("rc('rps_paper', 'p\\nq\\n')", "0"), ("'Type one of r, p, s, or q.' in run('rps_paper', 'x\\nq\\n')", "True"),
 # range
 ("list(range(5))", "[0, 1, 2, 3, 4]"), ("len(range(5))", "5"), ("list(range(0))", "[]"), ("range(10) == range(0, 10) == range(0, 10, 1)", "True"),
 ("list(range(12, 16))", "[12, 13, 14, 15]"), ("len(range(12, 16))", "4"), ("list(range(16, 12))", "[]"), ("list(range(0, 10, 2))", "[0, 2, 4, 6, 8]"),
 ("list(range(0, 10, 3))", "[0, 3, 6, 9]"), ("len(range(0, 10, 3))", "4"), ("list(range(-10, -100, -30))", "[-10, -40, -70]"),
 ("list(reversed(range(1, 10, 2)))", "[9, 7, 5, 3, 1]"), ("list(range(5, -1, -1))", "[5, 4, 3, 2, 1, 0]"), ("list(range(5, 0))", "[]"),
 ("msg('range(2.5)')", repr("TypeError: 'float' object cannot be interpreted as an integer")), ("msg('range(0, 10, 0)')", repr("ValueError: range() arg 3 must not be zero")),
 ("repr(range(10))", repr("range(0, 10)")), ("range(10) == list(range(10))", "False"), ("isinstance(range(3), list)", "False"), ("sum(range(4))", "6"),
 ("__import__('sys').getsizeof(range(10)) == __import__('sys').getsizeof(range(10 ** 6))", "True"),
 ("'hello'[1:3]", repr("el")), ("len(range(0, 24))", "24"), ("list(range(0, 5)) + list(range(5, 10)) == list(range(10))", "True"), ("list(range(1, 11))", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"),
 ("(lambda r: [10 in r, 11 in r, r[5], r.index(10), r[-1], r[:5]])(range(0, 20, 2))", "[True, False, 10, 5, 18, range(0, 10, 2)]"),
 # enumerate, zip, unpacking
 ("list(enumerate(['Spring', 'Summer', 'Fall', 'Winter']))", "[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]"),
 ("run('for_pairs')", repr("0 tic\n1 tac\n2 toe\n")), ("list(enumerate(['tic', 'tac', 'toe'], start=1))", "[(1, 'tic'), (2, 'tac'), (3, 'toe')]"),
 ("type(enumerate('ab')).__name__", repr("enumerate")), ("next(enumerate('ab'))", "(0, 'a')"), ("list(zip('abc', [1, 2]))", "[('a', 1), ('b', 2)]"),
 ("msg(\"list(zip('ab', [1], strict=True))\")", repr("ValueError: zip() argument 2 is shorter than argument 1")),
 ("msg(\"list(zip('a', [1, 2], strict=True))\")", repr("ValueError: zip() argument 2 is longer than argument 1")),
 ("run('unpack_ok')", repr("1 2\n")), ("run('t_pack')", repr("(12345, 54321, 'hello!')\n")),
 ("msg('x, y = (1,)')", repr("ValueError: not enough values to unpack (expected 2, got 1)")),
 # iterables, iterators, collections
 ("list({'a': 1, 'b': 2})", "['a', 'b']"), ("msg('iter(5)')", repr("TypeError: 'int' object is not iterable")),
 ("run('iter_next')", repr("10\n20\n")), ("err('iter_next')", repr("StopIteration")), ("msg('next([1, 2])')", repr("TypeError: 'list' object is not an iterator")), ("next(iter([]), 'done')", repr("done")),
 ("(lambda it: [list(it), list(it)])(iter([1, 2]))", "[[1, 2], []]"),
 ("[[10, 20, 30][0], (10, 20, 30)[-1]]", "[10, 30]"), ("msg('{\"a\": 1}[0]')", repr("KeyError: 0")),
 ("run('append')", repr("[1, 2, 3]\n")), ("run('list_set')", repr("[99, 2]\n")), ("err('tuple_set')", repr("TypeError: 'tuple' object does not support item assignment")),
 ("err('str_set').split(':')[0]", repr("TypeError")), ("[(0, 'tic')[0], len(('hello',)), type(('hello')).__name__, len(())]", "[0, 1, 'str', 0]"),
 ("run('dict_ops')", repr("{'Ada': 'active'} 1\n")), ("list({'Ada': 'active', 'Can': 'inactive'})", "['Ada', 'Can']"),
 ("msg(\"{'Ada': 'active'}['Eda']\")", repr("KeyError: 'Eda'")), ("list({'b': 1, 'a': 2})", "['b', 'a']"),
 # break, continue, exit, interrupt, return
 ("run('break_value')", repr("3\n")), ("msg('break')", repr("SyntaxError: 'break' outside loop")), ("msg('continue')", repr("SyntaxError: 'continue' not properly in loop")),
 ("rc('exit0')", "0"), ("rc('exit3')", "3"), ("rc('exitmsg')", "1"), ("err('exitmsg')", repr("bad")), ("run('exitfinally')", repr("cleanup\n")), ("run('exitcatch')", repr("caught 3\nstill running\n")),
 ("run('exitexample', 'hi\\nexit\\n').count('You typed hi.')", "1"), ("rc('exitexample', 'hi\\nexit\\n')", "0"), ("msg('sys.exit()')", repr("NameError: name 'sys' is not defined")),
 ("run('kbint')", repr("stopped\n")), ("err('kbint_loose')", repr("KeyboardInterrupt")), ("[issubclass(ValueError, Exception), issubclass(SystemExit, Exception), issubclass(KeyboardInterrupt, Exception)]", "[True, False, False]"),
 ("run('finally_kb')", repr("Goodbye, world!\n")), ("err('finally_kb')", repr("KeyboardInterrupt")),
 ("run('return_loop')", repr("4\nNone\n")), ("msg('return')", repr("SyntaxError: 'return' outside function")),
 ("msg('continue')", repr("SyntaxError: 'continue' not properly in loop")),
 # loop else, scope, ending
 ("run('primes')", repr(_L("2 is a prime number", "3 is a prime number", "4 equals 2 * 2", "5 is a prime number", "6 equals 2 * 3", "7 is a prime number", "8 equals 2 * 4", "9 equals 3 * 3"))),
 ("run('forelse_empty')", repr("else\n")), ("run('whileelse')", repr("else ran 0\n")), ("run('break_else')", repr("after\n")), ("run('break_cond')", repr("3 True\n")),
 ("run('iscope')", repr("2\n")), ("err('jscope')", repr("NameError: name 'j' is not defined")), ("run('overwrite')", repr("".join("%d\n" % i for i in range(10)))), ("run('clobber')", repr("2\n")),
 # exceptions, finally, warning
 ("msg('10 * (1/0)')", repr("ZeroDivisionError: division by zero")), ("run('handle')", repr("bad number\n")), ("run('tryfinally_exc')", repr("cleanup\n")), ("err('tryfinally_exc').split(':')[0]", repr("ValueError")),
 ("run('finally_order')", repr("cleanup 0\ncleanup 1\n")), ("run('finally_return')", repr("42\n")), ("run('finally_break')", repr("done\n")),
 ("warnline('finally_break')", "(\"SyntaxWarning: 'break' in a 'finally' block\" if sys.version_info >= (3, 14) else '')"),
 ("run('warn_finally')", "('1\\n' if sys.version_info >= (3, 14) else '0\\n')"), ("warnline('finally_ok')", repr("")),
 # modules and imports
 ("run('import5')", repr(_L("4", "10", "9", "3", "6"))), ("run('multi')", repr("random sys os math\n")), ("run('from_math')", repr("4.0\n")), ("err('from_math').startswith(\"NameError: name 'math' is not defined\")", "True"),
 ("run('as_math')", repr("5.0\nmath\n")), ("run('star_pow')", repr("8\n8.0\n")), ("msg(\"exec(PG['star_func'])\")", repr("SyntaxError: import * only allowed at module level")),
 ("len(__import__('random').__all__)", "26"), ("msg('random.randint(1, 10)')", repr("NameError: name 'random' is not defined")),
 ("msg(\"__import__('no_such_module_x')\")", repr("ModuleNotFoundError: No module named 'no_such_module_x'")),
 ("msg(\"exec('from math import nope')\").startswith(\"ImportError: cannot import name 'nope' from 'math'\")", "True"),
 ("[type(__import__('math')).__name__, __import__('math').__name__, __import__('random').__name__]", "['module', 'math', 'random']"), ("run('dunder_main')", repr("__main__\n")),
 ("len('hello')", "5"), ("msg('math.sqrt(16)')", repr("NameError: name 'math' is not defined")), ("__import__('math').sqrt(16)", "4.0"),
 ("'sqrt' in dir(__import__('math'))", "True"), ("msg(\"__import__('math').nope\")", repr("AttributeError: module 'math' has no attribute 'nope'")),
 ("run('modules_cache')", repr("False\nTrue\n")), ("pathfirst()", "True"),
 ("clash().startswith(\"AttributeError: module 'random' has no attribute 'randint'\")", "True"), ("('consider renaming' in clash())", "(sys.version_info >= (3, 14))"),
 ("err('shadow_list').split(':')[0]", repr("TypeError")),
 ("run('seed')", repr("True\n")), ("run('randint_ends')", repr("[1, 2, 3]\n[1, 2]\n")),
 # walrus and style
 ("run('walrus')", repr("abc\ndef\ngh\n")), ("run('walrus') == run('walrus_old')", "True"), ("(lambda: [(n := 5) + 1][0])()", "6"), ("msg(\"compile('y := 5', '<s>', 'exec')\").split(':')[0]", repr("SyntaxError")),
 # hazards
 ("err('mutate_dict')", repr("RuntimeError: dictionary changed size during iteration")), ("run('mutate_dict_copy')", repr("{'Ada': 'active'}\n")),
 ("run('mutate_list')", repr("[1, 2, 3]\n")), ("run('mutate_list_new')", repr("[1, 3]\n")),
]
# the input-output example of each concept is itself a claim and is executed
CHECKS += [(n[4][2][0], n[4][2][1]) for n in NODES if n[4] and n[4][2]]
# errors the texts name: (code run in a fresh namespace, exception class)
RAISES = [("range(2.5)", "TypeError"), ("range(0, 10, 0)", "ValueError"), ("range(3) + range(3)", "TypeError"), ("range(3) * 2", "TypeError"),
 ("list(zip('ab', [1], strict=True))", "ValueError"), ("x, y = (1,)", "ValueError"), ("a, b = (1, 2, 3)", "ValueError"), ("for i in 5:\n    pass", "TypeError"), ("iter(5)", "TypeError"),
 ("next([1, 2])", "TypeError"), ("next(iter([]))", "StopIteration"), ("{'a': 1}[0]", "KeyError"), ("{[1]: 2}", "TypeError"), ("t = (1, 2)\nt[0] = 99", "TypeError"), ("s = 'abc'\ns[0] = 'x'", "TypeError"),
 ("break", "SyntaxError"), ("continue", "SyntaxError"), ("return", "SyntaxError"), ("sys.exit()", "NameError"), ("random.randint(1, 10)", "NameError"),
 ("math.sqrt(16)", "NameError"), ("__import__('no_such_module_x')", "ModuleNotFoundError"), ("exec('from math import nope')", "ImportError"), ("__import__('math').nope", "AttributeError"),
 ("exec(PG['star_func'])", "SyntaxError"), ("compile('y := 5', '<s>', 'exec')", "SyntaxError"), ("10 * (1/0)", "ZeroDivisionError"), ("int('x')", "ValueError"),
 ("while never_set != 1:\n    pass", "NameError"), ("for num in range(101):\n    total = total + num", "NameError"), ("exec(PG['mutate_dict'])", "RuntimeError"),
 ("exec(PG['kbint_loose'])", "KeyboardInterrupt"), ("exec(PG['exitmsg'])", "SystemExit")]

PRELUDE = '''
import subprocess, sys, os, tempfile
def _p(src, inp="", t=20):
    return subprocess.run([sys.executable, "-c", src], input=inp, capture_output=True, text=True, timeout=t)
def run(n, inp=""): return _p(PG[n], inp).stdout
def rc(n, inp=""): return _p(PG[n], inp).returncode
def err(n, inp=""):
    ls = [x for x in _p(PG[n], inp).stderr.splitlines() if x.strip()]
    return ls[-1] if ls else ""
def stuck(n):
    try:
        _p(PG[n], "", 1); return False
    except subprocess.TimeoutExpired:
        return True
def warnline(n):
    ls = [x[x.index("SyntaxWarning"):] for x in _p(PG[n]).stderr.splitlines() if "SyntaxWarning" in x]
    return ls[0] if ls else ""
def msg(code):
    try:
        exec(code, {"PG": PG}); return "no error"
    except SyntaxError as e:
        return "SyntaxError: " + e.msg
    except BaseException as e:
        return type(e).__name__ + ": " + str(e)
def clash():
    d = tempfile.mkdtemp()
    open(os.path.join(d, "random.py"), "w").write("x = 1\\n"); open(os.path.join(d, "main.py"), "w").write("import random\\nrandom.randint(1, 10)\\n")
    r = subprocess.run([sys.executable, os.path.join(d, "main.py")], capture_output=True, text=True, cwd=tempfile.gettempdir())
    return [x for x in r.stderr.splitlines() if x.strip()][-1]
def pathfirst():
    d = os.path.realpath(tempfile.mkdtemp()); f = os.path.join(d, "prog.py"); open(f, "w").write(PG["pathfirst_probe"])
    return os.path.realpath(subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=tempfile.gettempdir()).stdout.strip()) == d
'''

def facet_text(paras):
    """paragraphs joined by a blank line; the question a paragraph answers is a writing guide, it is not printed"""
    return "\n\n".join(t for f, t in paras)


# ---- what the generic chapter builder (sen0414_chapter_build_v1_0_0.py) needs besides NODES ----
CHAPTER = "03"
OWNERS = [("RangeStartStop", "RangeStop"), ("RangeStep", "RangeStop"), ("RangeDescending", "RangeStep"), ("MultipleImport", "ImportStatement"),
          ("StarImport", "ImportStatement"), ("FromImport", "ImportStatement"), ("ForWhileEquivalence", "ForStatement"), ("IteratorObject", "IterableObject")]
ERRORS = [("Accumulator", "exec('for num in range(101):\\n    total = total + num') raises NameError: name 'total' is not defined"),
          ("RangeStep", "range(0, 10, 0) raises ValueError: range() arg 3 must not be zero"),
          ("RangeStop", "range(2.5) raises TypeError: 'float' object cannot be interpreted as an integer"),
          ("ZipStrict", "list(zip('ab', [1], strict=True)) raises ValueError: zip() argument 2 is shorter than argument 1"),
          ("IterableObject", "iter(5) raises TypeError: 'int' object is not iterable"),
          ("IteratorObject", "next([1, 2]) raises TypeError: 'list' object is not an iterator"),
          ("DictionaryValue", "{'Ada': 'active'}['Eda'] raises KeyError: 'Eda'"),
          ("TupleValue", "exec('t = (1, 2)\\nt[0] = 99') raises TypeError: 'tuple' object does not support item assignment"),
          ("BreakStatement", "exec('break') raises SyntaxError: 'break' outside loop"),
          ("ContinueStatement", "exec('continue') raises SyntaxError: 'continue' not properly in loop"),
          ("ReturnFromLoop", "exec('return') raises SyntaxError: 'return' outside function"),
          ("ExitFunction", "sys.exit() raises NameError: name 'sys' is not defined"),
          ("LoopVariableScope", "exec('for j in []:\\n    pass\\nprint(j)') raises NameError: name 'j' is not defined"),
          ("StarImport", "exec('def f():\\n    from math import *') raises SyntaxError: import * only allowed at module level"),
          ("ModuleNamespace", "__import__('math').nope raises AttributeError: module 'math' has no attribute 'nope'"),
          ("StandardLibrary", "math.sqrt(16) raises NameError: name 'math' is not defined"),
          ("ImportStatement", "__import__('no_such_module_x') raises ModuleNotFoundError: No module named 'no_such_module_x'"),
          ("MutationWhileIterating", "exec('users = {1: 2}\\nfor u in users:\\n    del users[u]') raises RuntimeError: dictionary changed size during iteration")]
# every error condition above is executed too: the code before " raises " must raise the class and message that follow
CHECKS += [("msg(%r)" % e.split(" raises ")[0], repr(e.split(" raises ")[1])) for l, e in ERRORS]
CQS = ["Which constructs repeat a block, and what decides when each one stops?",
       "Which statements leave or skip part of a loop, and what do they leave behind?",
       "Which operations raise an error, and which error with which message?",
       "Which concepts reach beyond the 3rd edition into current Python, and on what source?",
       "Which terms does the chapter use without defining them, and where are they defined here?"]
PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 3 through the Stage 1 research artefact; the loop mechanics, the module "
              "background and the modern-practice branch are drawn from that artefact's secondary sources (the Python documentation and PEPs), not from the book.")
DOC_TITLE = "Loops and modules for an advanced course"
DOC_ABOUT = "This document renews chapter 3 of the 3rd edition for an advanced course, defining the loop and module terms the book uses without explaining them and pairing its programs with the Python students now run (Sweigart, 2025)."
INTERPRETERS = "CPython 3.12.11 and CPython 3.14.4"
CHANGE = ("1.1.0 (MINOR) adds every term, tool and idea that the chapter text uses without explaining it, keeps every concept of 1.0.0, rewrites each concept as "
          "four to six connected paragraphs with author-year citations, and executes every number, output and error message quoted, under both interpreters.")

if __name__ == "__main__":
    import subprocess, sys, re, os, json
    py = sys.argv[1] if len(sys.argv) > 1 else "python3.14"
    code = "PG = " + repr(PG) + "\n" + PRELUDE + ("import json\nout = []\nfor e, x in %r:\n    try:\n        got = repr(eval(e))\n        want = repr(eval(x)) if x.startswith('(') and 'version_info' in x else x\n"
            "        out.append((e, got == want or got + ' != ' + want))\n    except BaseException as ex:\n        out.append((e, 'raised ' + type(ex).__name__ + ': ' + str(ex)))\n"
            "for e, x in %r:\n    try:\n        exec(e, {'PG': PG})\n        out.append((e, 'no error'))\n    except BaseException as ex:\n        out.append((e, type(ex).__name__ == x or type(ex).__name__))\nprint(json.dumps(out))") % (CHECKS, RAISES)
    r = subprocess.run([py, "-c", code], capture_output=True, text=True)
    try: res = json.loads(r.stdout)
    except Exception: print(r.stdout[-2000:], r.stderr[-2000:]); raise SystemExit(1)
    bad = [x for x in res if x[1] is not True]
    print(len(res), "claims executed under", subprocess.run([py, "--version"], capture_output=True, text=True).stdout.strip(), "- failures:", bad)
    ids = [n[0] for n in NODES]; assert len(ids) == len(set(ids))
    print(len(NODES), "concepts;", sum(len(n[5]) for n in NODES), "paragraphs;", sum(len(t.split()) for n in NODES for f, t in n[5]), "words")
    rp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "03-materials", "ch03", "rdodi", "sen0414_ch03_research_v1_1_0.ttl")
    if os.path.exists(rp):
        R = open(rp).read(); miss = sorted({c for c in CITES.values() if c not in R and c.strip("()") not in R})
        print("citations resolving in the research record:", len(CITES) - len(miss), "of", len(CITES), miss or "")
    sys.exit(1 if bad else 0)
