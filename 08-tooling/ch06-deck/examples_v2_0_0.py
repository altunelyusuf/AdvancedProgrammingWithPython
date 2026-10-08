__version__ = "2.0.0"
# Every console row and every whole program the SEN0414 chapter 6 (Lists) lecture deck version 2.0.0 shows.
# Outputs come from executing them (examples_run_v2_0_0.py), never from typing. A console group is a list of
# statements run in order in ONE namespace, exactly as deck_check_v1_0_1.py re-runs the '>>>' rows of a slide; each
# row is one line, so a row is either an expression (its repr is shown) or a statement (nothing is shown).
EX = {
    "Index": [
        "spam = ['cat', 'bat', 'rat', 'elephant']",
        "spam[0]", "spam[3]", "spam[-1]", "spam[-3]", "len(spam)",
        "spam[10]",
    ],
    "Half": [
        "s = list(range(10))",
        "s[2:5]", "len(s[2:5])", "s[0:3] + s[3:10] == s",
    ],
    "Slice": [
        "spam = ['cat', 'bat', 'rat', 'elephant']",
        "spam[1:3]", "spam[:2]", "spam[2:]", "spam[::2]", "spam[::-1]", "spam[:]",
        "list(range(10))[::3]",
    ],
    "Change": [
        "spam = ['cat', 'bat', 'rat', 'elephant']",
        "spam[1] = 'aardvark'", "spam.append('moose')", "spam.insert(1, 'chicken')", "spam",
        "spam.pop()", "del spam[0]", "spam.remove('rat')", "spam",
    ],
    "Combine": [
        "spam = [1, 2, 3]",
        "spam + ['A', 'B']", "['X', 'Y'] * 3", "spam += [4]", "spam",
        "spam.extend(['A', 'B'])", "spam",
    ],
    "Search": [
        "pets = ['Zophie', 'Pooka', 'Fat-tail', 'Pooka']",
        "'Pooka' in pets", "'Cat' not in pets", "pets.index('Pooka')", "pets.index('Cat')",
        "[] and [][0] == 'cat'",
    ],
    "Sort": [
        "nums = [2, 5, 3.14, 1, -7]",
        "nums.sort()", "nums", "nums.sort(reverse=True)", "nums",
        "sorted(['a', 'z', 'A', 'Z'])", "sorted(['a', 'z', 'A', 'Z'], key=str.lower)",
        "[1, 'a'].sort()",
    ],
    "Loop": [
        "supplies = ['pens', 'staplers', 'flamethrowers', 'binders']",
        "list(enumerate(supplies))",
        "[len(s) for s in supplies]",
        "[i for i in range(len(supplies)) if supplies[i] == 'binders']",
    ],
    "Mutation": [
        "items = ['a', 'b', 'c', 'd']",
        "[items.remove(x) for x in items]", "items",
        "squares = [x**2 for x in range(1, 7)]", "squares",
        "[x for x in range(10) if x % 2 == 0]",
    ],
    "Unpack": [
        "size, color, disposition = ['fat', 'gray', 'loud']",
        "(size, color, disposition)",
        "first, *rest = [1, 2, 3, 4]", "(first, rest)",
        "a, b = 'x', 'y'", "a, b = b, a", "(a, b)",
        "a, b = [1, 2, 3]",
    ],
    "Alias": [
        "spam = [0, 1, 2, 3]", "eggs = spam", "eggs[1] = 'Hello!'", "spam", "eggs is spam",
        "change = lambda p: p.append('Hello')", "nums = [1, 2, 3]", "change(nums)", "nums",
    ],
    "Copy": [
        "import copy", "grid = [[1, 2], [3, 4]]", "shallow = copy.copy(grid)", "deep = copy.deepcopy(grid)",
        "grid[0][0] = 99", "shallow[0][0]", "deep[0][0]",
        "board = [[0] * 3] * 2", "board[0][0] = 9", "board",
    ],
    "Shuffle": [
        "import random", "from collections import Counter", "random.seed(1938)", "cards = list('abc')",
        "deal = lambda: (random.shuffle(cards), ''.join(cards))[1]",
        "c = Counter(deal() for _ in range(6000))",
        "sorted(c)", "[c[k] - 1000 for k in sorted(c)]",
    ],
}

# whole programs: name -> (code, [inputs per run]); none of them reads input, so each has one run with no inputs
PROGRAMS = {
    "magic8ball_v1_0_0.py": ("""import random

# the answers live in a list, so adding an answer needs no new code
messages = ['It is certain', 'It is decidedly so', 'Yes definitely',
            'Reply hazy try again', 'Ask again later', 'Concentrate and ask again',
            'My reply is no', 'Outlook not so good', 'Very doubtful']

random.seed(1946)  # fixed so every run shows the same three answers
for _ in range(3):
    print(messages[random.randint(0, len(messages) - 1)])  # a random index
""", [[]]),
    "matrix_v1_0_0.py": ("""import random
random.seed(7)  # fixed, so the rain falls the same way each run
WIDTH = 20
counters = [0] * WIDTH  # rows of rain still to draw in each column
for row in range(5):
    line = ''
    for col in range(WIDTH):
        if counters[col] == 0 and random.random() < 0.25:
            counters[col] = random.randint(2, 4)  # a new stream
        line += random.choice('01') if counters[col] > 0 else ' '
        counters[col] = max(0, counters[col] - 1)
    print(line.rstrip())
""", [[]]),
    "commacode_v1_0_0.py": ("""def list_to_text(items):
    # fewer than three items need no commas
    if len(items) < 3:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ', and ' + items[-1]  # slice off the last

tests = [['apples', 'bananas', 'tofu', 'cats'], ['tea', 'toast'], ['spam'], []]
for t in tests:
    print(repr(list_to_text(t)))
""", [[]]),
    "coinstreaks_v1_0_0.py": ("""import random
random.seed(6)  # fixed so the estimate is the same on every run
streaks = 0
for experiment in range(10000):
    flips = [random.choice('HT') for _ in range(100)]  # one experiment
    run = longest = 1
    for i in range(1, 100):
        run = run + 1 if flips[i] == flips[i - 1] else 1  # extend or restart
        longest = max(longest, run)
    if longest >= 6:
        streaks += 1
print('Chance of a streak of 6: %s %%' % (100 * streaks / 10000))
""", [[]]),
}
