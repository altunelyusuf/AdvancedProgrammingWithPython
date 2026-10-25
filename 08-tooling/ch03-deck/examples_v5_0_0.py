"""Chapter 3 deck examples, version 5.0.0: the code examples of the chapter 3 lecture deck (Loops).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained (it imports what it uses), uses only the Python standard library and needs no keyboard:
typed answers are scripted with iter() and next(). Nothing here carries a result; deck_build_v5_0_0.py runs the code and
takes every printed result from the run."""
__version__ = "5.0.0"

EXAMPLES = [
    # ---------------------------------------------------------------- part 1: while
    dict(id="while", name="while repeats while its test is true", title="while: repeat as long as the test is true", part=1, visual="while",
         concepts=["while Loop Statements", "while", "Loop", "Iteration"],
         groups=[
             (["spam = 0", "while spam < 5:"],
              "spam starts at 0. The while statement tests spam < 5 before every pass through its block."),
             (["    print('pass', spam, 'spam < 5 is', spam < 5)", "    spam = spam + 1"],
              "The indented lines are the block. It prints the pass and adds 1; without the second line the loop never stops."),
             (["print('stop: spam is', spam, 'and spam < 5 is', spam < 5)"],
              "When the test turns False, Python skips the block and goes on below it."),
         ]),
    dict(id="accumulator", name="An accumulator adds 1 to 100", title="An accumulator adds up 1 to 100", part=1, visual="accumulator",
         concepts=["Accumulator", "Loop"],
         groups=[
             (["total, n, steps = 0, 1, []", "while n <= 100:"],
              "total is the accumulator: it starts at 0 and collects a little at every pass. n counts from 1 to 100."),
             (["    total = total + n", "    if n % 20 == 0:", "        steps.append(total)", "    n = n + 1"],
              "Every pass adds n to total. After every twentieth number the program keeps a snapshot of the running total."),
             (["print(total, 100 * 101 // 2, steps)"],
              "The second number is Gauss's formula n(n+1)/2. The loop and the formula agree."),
         ]),
    dict(id="breakloop", name="while True leaves with break", title="while True runs until break leaves it", part=1, visual="breakloop",
         concepts=["break", "Early exit"],
         groups=[
             (["answers = iter(['', 'Al', 'Alice'])", "while True:"],
              "iter() stands in for a typing person: each next(answers) is one typed answer."),
             (["    name = next(answers)", "    print('typed', repr(name), '- is it Alice?', name == 'Alice')"],
              "Each pass reads one answer and prints whether it is the right one."),
             (["    if name == 'Alice':", "        break", "print('Welcome,', name)"],
              "break leaves the loop at once, although the test is still True. The program goes on after the block."),
         ]),
    dict(id="continue", name="continue returns to the test", title="continue skips the rest of one pass", part=1, visual="continue",
         concepts=["continue", "Loop"],
         groups=[
             (["n, shown, skipped = 0, [], []", "while n < 8:", "    n = n + 1"],
              "n counts from 1 to 8. The lists shown and skipped remember what happened to each number."),
             (["    if n % 2 == 0:", "        skipped.append(n)", "        continue", "    shown.append(n)"],
              "For an even n, continue jumps straight back to the while test. The line after it is skipped in that pass."),
             (["print('shown', shown, 'skipped', skipped)"],
              "Odd numbers reach the end of the block; even numbers never do."),
         ]),
    dict(id="walrus", name="The walrus names a value in the test", title="The assignment expression in a loop test", part=1, visual="walrus",
         concepts=["Assignment expression", "while"],
         groups=[
             (["import io", "f = io.StringIO('Loops repeat work.')"],
              "StringIO makes a file-like object from a text. It plays the part of a file that is read in small pieces."),
             (["while chunk := f.read(5):", "    print(repr(chunk))"],
              "The walrus := reads five characters and names them chunk in one expression. The loop ends when read gives an empty string."),
             (["print(repr(f.read(5)), bool(''))"],
              "At the end of the text read gives '', and an empty string counts as False."),
         ]),
    # ---------------------------------------------------------------- part 2: for and range
    dict(id="forrange", name="for takes the values of range(5)", title="for: one value of range(5) per pass", part=2, visual="forrange",
         concepts=["for", "for Loops and the range() Function", "Loop variable", "range()"],
         groups=[
             (["total = 0", "for i in range(5):"],
              "The for statement takes the values of range(5) one by one and puts each into the loop variable i."),
             (["    total = total + i", "    print('i is', i, 'total is', total)"],
              "No counter has to be started or advanced by hand. The block runs once for each value."),
             (["print('after the loop i is still', i)"],
              "The loop variable is not deleted when the loop ends. It keeps the last value, 4."),
         ]),
    dict(id="rangeargs", name="range(start, stop, step)", title="range(start, stop, step)", part=2, visual="rangeargs",
         concepts=["range()", "Half-open interval"],
         groups=[
             (["print(list(range(5)), list(range(2, 8)))"],
              "One argument is the stop; two arguments are start and stop. The stop value itself is never included."),
             (["print(list(range(0, 10, 3)), list(range(5, 0, -2)))"],
              "The third argument is the step. A negative step counts down."),
             (["print(list(range(0, 3)) + list(range(3, 7)) == list(range(7)))"],
              "Half-open ranges meet without gap or overlap: 0 to 3 and 3 to 7 make 0 to 7."),
         ]),
    dict(id="lazyrange", name="range is lazy", title="range describes numbers; it does not store them", part=2, visual="lazyrange",
         concepts=["range()", "Sequence"],
         groups=[
             (["r = range(10 ** 9)", "print(len(r), r[999999999])"],
              "A billion numbers are described, not stored. len and indexing answer at once."),
             (["print(123456789 in r, r[:3])", "print(r, type(r).__name__)"],
              "The in test is arithmetic, not a search. Slicing a range gives another range, not a list."),
         ]),
    # ---------------------------------------------------------------- part 3: what a for loop visits
    dict(id="listtuple", name="for visits a list and a tuple", title="for visits a list and a tuple", part=3, visual="listtuple",
         concepts=["List", "Tuple", "Sequence to iterate", "Iterable"],
         groups=[
             (["pets = ['cat', 'tiger', 'owl']", "for pet in pets:", "    print(pet.upper(), len(pet))"],
              "A list is visited in order, item by item. Each pass shows the loop variable pet in capitals and its length."),
             (["point = (3, 4)", "for coordinate in point:", "    print(coordinate * 2)"],
              "A tuple is visited in the same way, but it cannot be changed. Lists use brackets and tuples use parentheses."),
         ]),
    dict(id="dictloop", name="for visits a dictionary", title="for visits the pairs of a dictionary", part=3, visual="dictloop",
         concepts=["Dictionary", "Sequence unpacking"],
         groups=[
             (["ages = {'cat': 4, 'dog': 7, 'owl': 2}", "for name, age in ages.items():", "    print(name, 'is', age)"],
              "items() gives key and value pairs. The loop variables name and age unpack each pair into two names."),
             (["print(sum(ages.values()), list(ages))"],
              "values() gives only the values. A loop over the dictionary alone visits its keys."),
         ]),
    dict(id="enumzip", name="enumerate and zip", title="enumerate and zip replace index arithmetic", part=3, visual="enumzip",
         concepts=["Sequence unpacking", "Sequence"],
         groups=[
             (["names = ['ann', 'bo', 'cy']", "scores = [90, 75, 82]"],
              "Two lists that belong together by position."),
             (["for i, name in enumerate(names, start=1):", "    print(i, name)"],
              "enumerate hands out a counter and the item together, so range(len(names)) is not needed."),
             (["for name, score in zip(names, scores):", "    print(name, score)"],
              "zip walks two lists side by side and gives one pair per pass."),
         ]),
    dict(id="zipstrict", name="zip checks lengths with strict", title="zip: stop silently, or insist on equal lengths", part=3, visual="zipstrict",
         concepts=["Sequence unpacking", "Exception"],
         groups=[
             (["try:", "    for a, b in zip([1, 2, 3], ['x', 'y'], strict=True):", "        print(a, b)"],
              "strict=True makes zip check the lengths. The first two pairs are fine."),
             (["except ValueError as err:", "    print('ValueError:', err)"],
              "When one list runs out first, zip raises a ValueError (Python 3.10 and later)."),
             (["print(list(zip([1, 2, 3], ['x', 'y'])))"],
              "Without strict, zip stops at the shorter list and the 3 is dropped without a word."),
         ]),
    dict(id="iterator", name="iter and next under every for", title="Under every for: iter and next", part=3, visual="iterator",
         concepts=["Iterator", "Iterable", "Exception"],
         groups=[
             (["it = iter(['a', 'b'])", "print(next(it), next(it))"],
              "iter asks a list for an iterator. Each next gives the following item. A for loop does this behind the scenes."),
             (["try:", "    next(it)", "except StopIteration:", "    print('exhausted')"],
              "When no items are left, next raises StopIteration. The for statement catches it and ends the loop quietly."),
             (["print(iter(it) is it, iter([1]) is [1])"],
              "An iterator returns itself from iter. An iterable such as a list gives a new iterator every time."),
         ]),
    dict(id="loopelse", name="else on a loop runs without break", title="break, and the else clause of a loop", part=3, visual="loopelse",
         concepts=["break", "Early exit", "Loop"],
         groups=[
             (["for nums in ([3, 5, 8], [3, 5]):", "    for n in nums:"],
              "The outer loop takes two lists. The inner loop looks for the first even number in each."),
             (["        if n % 2 == 0:", "            print(nums, 'first even', n)", "            break"],
              "break leaves only the inner loop. The outer loop carries on with the next list."),
             (["    else:", "        print(nums, 'no even number')"],
              "The else belongs to the inner for. It runs only when the loop ended without a break."),
         ]),
    # ---------------------------------------------------------------- part 4: modules and leaving early
    dict(id="importrandom", name="import random with a seed", title="import random: a seeded dice roll", part=4, visual="importrandom",
         concepts=["Importing Modules", "Module"],
         groups=[
             (["import random", "random.seed(42)", "rolls = []"],
              "import random opens a standard module. seed(42) fixes the starting point, so every run gives the same rolls."),
             (["for _ in range(6):", "    rolls.append(random.randint(1, 6))"],
              "randint(1, 6) includes both ends. The underscore says that the loop variable is not used."),
             (["print(rolls, random.__name__, type(random).__name__)"],
              "A module is an object with a name. Its contents are reached with a dot."),
         ]),
    dict(id="importforms", name="import forms and namespaces", title="Two import forms, two namespaces", part=4, visual="importforms",
         concepts=["Namespace", "Importing Modules"],
         groups=[
             (["import math", "from math import sqrt as root"],
              "import math brings in the module name. from ... import ... as ... brings in one name under a new name."),
             (["print(math.sqrt(16), root(16))"],
              "Both reach the same function. math.sqrt names its module; root does not."),
             (["try:", "    sqrt(16)", "except NameError as err:", "    print('NameError:', err)"],
              "The name sqrt was never brought into this namespace, so Python cannot find it."),
         ]),
    dict(id="importerror", name="A module that cannot be found", title="When import fails: the module search path", part=4, visual="importerror",
         concepts=["Module search path", "Exception"],
         groups=[
             (["import sys", "try:", "    import nosuchmodule"],
              "import looks for the module in every folder of the module search path, one after the other."),
             (["except ModuleNotFoundError as err:", "    print(type(err).__name__, '-', err)"],
              "When no folder holds it, Python raises ModuleNotFoundError and names the module."),
             (["print(type(sys.path).__name__, len(sys.path) > 0)"],
              "The search path is an ordinary list of folders, kept in sys.path."),
         ]),
    dict(id="sysexit", name="sys.exit raises SystemExit", title="sys.exit() ends a program with an exit status", part=4, visual="sysexit",
         concepts=["Ending a Program Early with sys.exit()", "Exit status", "Exception"],
         groups=[
             (["import sys", "try:", "    print('working')", "    sys.exit(3)", "    print('never printed')"],
              "sys.exit() stops the program. The number 3 is the exit status; 0 means success, any other number means a problem."),
             (["except SystemExit as err:", "    print('SystemExit with code', err.code)"],
              "sys.exit() works by raising the exception SystemExit, so a program can even catch it."),
             (["finally:", "    print('finally still runs')"],
              "Because it is an exception, the finally clause still runs on the way out."),
         ]),
    # ---------------------------------------------------------------- part 5: two short programs
    dict(id="guess1", name="Guess the Number: the loop", title="Guess the Number: at most six guesses", part=5, visual="guess1",
         concepts=["A Short Program: Guess the Number", "range()", "break"],
         groups=[
             (["import random", "random.seed(7)", "secret = random.randint(1, 20)", "guesses = iter([10, 15, 12, 11])"],
              "The secret is drawn from 1 to 20. A scripted iterator replaces the person who types the guesses."),
             (["for taken in range(1, 7):", "    guess = next(guesses)", "    if guess == secret:", "        break"],
              "The player gets at most six guesses. A right guess leaves the loop with break."),
             (["    print(guess, 'low' if guess < secret else 'high')", "print('stopped after', taken, 'guesses; secret', secret)"],
              "A wrong guess prints a hint. After the loop, taken still holds the number of the last pass."),
         ]),
    dict(id="guess2", name="Guess the Number: win or lose", title="Guess the Number: the ending, with for and else", part=5, visual="guess2",
         concepts=["A Short Program: Guess the Number", "break", "Loop"],
         groups=[
             (["secret = 11", "for guesses in ([10, 15, 12, 11], [1, 2, 3, 4, 5, 6]):"],
              "Two scripted games: one player finds the secret, the other never does."),
             (["    for taken, guess in enumerate(guesses, start=1):", "        if guess == secret:", "            print('Good job! You got it in', taken, 'guesses.')", "            break"],
              "enumerate counts the guesses from 1. A right guess prints the count and leaves the inner loop."),
             (["    else:", "        print('Nope. The number was', secret)"],
              "The else runs only when all six guesses were wrong and break never happened."),
         ]),
    dict(id="rps1", name="Rock, Paper, Scissors: one round", title="Rock, Paper, Scissors: one round", part=5, visual="rps1",
         concepts=["A Short Program: Rock, Paper, Scissors"],
         groups=[
             (["beats = {'r': 's', 'p': 'r', 's': 'p'}", "player, computer = 'p', 'r'"],
              "beats says which move each move defeats. The two moves are fixed here, so every run plays the same round."),
             (["if player == computer:", "    result = 'tie'", "elif beats[player] == computer:", "    result = 'win'", "else:", "    result = 'lose'"],
              "Three outcomes, one chain of tests: the same letter is a tie; a move that beats the other is a win."),
             (["print(player, 'vs', computer, '->', result)"],
              "One line reports the round."),
         ]),
    dict(id="rps2", name="Rock, Paper, Scissors: keeping score", title="Rock, Paper, Scissors: six rounds and a score", part=5, visual="rps2",
         concepts=["A Short Program: Rock, Paper, Scissors", "Accumulator"],
         groups=[
             (["beats = {'r': 's', 'p': 'r', 's': 'p'}", "score = {'win': 0, 'lose': 0, 'tie': 0}"],
              "The score is a dictionary of three accumulators, one for each outcome."),
             (["for player, computer in zip('rpsrps', 'rrrprs'):", "    key = 'win' if beats[player] == computer else 'lose'", "    if player == computer:", "        key = 'tie'"],
              "zip pairs the player's six moves with the computer's six. The key is win or lose first; the same letter turns it into a tie."),
             (["    print(player, 'vs', computer, key)", "    score[key] += 1", "print(score)"],
              "Each round prints its result and adds 1 to the matching accumulator."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
