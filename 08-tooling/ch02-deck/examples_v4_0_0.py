"""Chapter 2 deck examples, version 4.0.0: the code examples of the chapter 2 lecture deck (Flow Control).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained and uses only the Python standard library (the match examples need Python 3.10 or newer).
Nothing here carries a result; deck_build_v4_0_0.py runs the code and takes every printed result from the run.
`concepts` names the labels of the chapter research (sen0414_ch02_research_v1_1_0.ttl) that the slide teaches."""
__version__ = "4.0.0"

EXAMPLES = [
    dict(id="booleans", name="The two Boolean values", title="Boolean values: True and False", part=1, visual="booleans",
         concepts=["Boolean Values", "Boolean value"],
         groups=[
             (["print(type(True), type(False))", "print(True + True, int(False), True == 1)"],
              "True and False are the two values of the type bool. They behave like the numbers 1 and 0 in arithmetic."),
             (["print(bool(0), bool(1), bool(-3.5))"],
              "bool() turns any number into a Boolean value: zero gives False and every other number gives True."),
         ]),
    dict(id="comparison", name="The six comparison operators", title="Comparison operators", part=1, visual="comparison",
         concepts=["Comparison Operators", "Comparison operator", "==", "!=", "<", ">", "<=", ">="],
         groups=[
             (["x, y = 7, 9", "print(x == y, x != y, x < y)", "print(x <= y, x > y, x >= y)"],
              "Each comparison operator compares two values and returns a Boolean value. Here x is 7 and y is 9."),
         ]),
    dict(id="equality", name="Equality across types and strings", title="Equality, types and string order", part=1, visual="equality",
         concepts=["Comparison Operators", "Boolean value"],
         groups=[
             (["print(42 == 42.0, 42 == '42', 'hello' == 'Hello')"],
              "A number and a string never fit each other. Two strings are equal only if every letter has the same case."),
             (["print(0.1 + 0.2 == 0.3, 'apple' < 'banana', 'Z' < 'a')"],
              "Decimal fractions are stored in binary and can be a little off. Strings are ordered by character code, so capitals come first."),
         ]),
    dict(id="chained", name="Chained comparisons", title="Chained comparisons", part=1, visual="chained",
         concepts=["Comparison Operators", "Mixing Boolean and Comparison Operators"],
         groups=[
             (["age = 15", "print(10 < age < 20, 10 < age < 12)"],
              "A chain such as 10 < age < 20 means 10 < age and age < 20. Python reads it the way a mathematician writes it."),
             (["print(1 < 2 > 1.5, 3 > 2 > 5)"],
              "Every link of the chain must be true. In the second chain 2 > 5 is false, so the whole chain is false."),
         ]),
    dict(id="truthtable", name="The truth table of and, or", title="and, or: the truth table", part=2, visual="truthtable",
         concepts=["Boolean Operators", "Boolean operator", "and", "or"],
         groups=[
             (["for a in (True, False):", "    for b in (True, False):", "        print(a, b, a and b, a or b)"],
              "Two loops try all four pairs of values. The last two columns show what and and or give back for each pair."),
         ]),
    dict(id="notprec", name="not and the order of the operators", title="not, and the order of the operators", part=2, visual="notprec",
         concepts=["Boolean Operators", "not", "Mixing Boolean and Comparison Operators"],
         groups=[
             (["print(not True, not False, not not True)", "print(not 4 == 5, True or False and False)"],
              "not flips a value. It binds weaker than ==, so not 4 == 5 means not (4 == 5). And binds tighter than or."),
             (["print((True or False) and False, not (True and False))"],
              "Parentheses change the order. Use them whenever the order is not obvious to a reader."),
         ]),
    dict(id="mixing", name="Mixing Boolean and comparison operators", title="Mixing Boolean and comparison operators", part=2, visual="mixing",
         concepts=["Mixing Boolean and Comparison Operators", "Comparison operator", "Boolean operator"],
         groups=[
             (["age, member = 25, True", "print(age >= 18 and member)", "print(age < 13 or age > 65)", "print(not (age >= 18 and member))"],
              "Comparisons come first and give Boolean values. The Boolean operators then combine those values into one answer."),
         ]),
    dict(id="shortcircuit", name="Short-circuit and operand values", title="and, or: they stop early and return an operand", part=2, visual="shortcircuit",
         concepts=["and", "or", "Boolean operator"],
         groups=[
             (["print(1 or 1 / 0, 0 and 1 / 0)", "print('hi' and 'there', '' or 'default')"],
              "or stops at the first true operand and and stops at the first false one. The division by zero is never reached."),
             (["print(0 or [] or None, 1 and 2 and 3)"],
              "The result is an operand, not always True or False: the last one that was looked at."),
         ]),
    dict(id="truthiness", name="Truthiness of values", title="Truthiness: which values count as false", part=2, visual="truthiness",
         concepts=["Boolean Values", "Boolean value"],
         groups=[
             (["values = [0, 1, 0.0, '', 'a', [], [0], None]", "for v in values:", "    print(repr(v), bool(v))"],
              "Zero, the empty string, the empty list and None count as false. Everything else counts as true."),
             (["greeting = 'hello'", "print(greeting == True, bool(greeting))"],
              "Never write == True. A non-empty string is not equal to True, but it passes the test: write if greeting."),
         ]),
    dict(id="block", name="A block of statements", title="Blocks: the lines that belong to an if", part=3, visual="block",
         concepts=["Block", "Components of Flow Control", "if"],
         groups=[
             (["age = 70", "if age > 65:", "    print('senior')", "    print('discount')", "print('end')"],
              "The condition ends with a colon. The two lines indented under it form the block that runs only if the condition is true."),
         ]),
    dict(id="indent", name="Indentation decides the block", title="Indentation decides what belongs to the block", part=3, visual="indent",
         concepts=["Block", "Flow control statement"],
         groups=[
             (["x = 1", "if x > 3:", "    print('big')", "    print('inside the block')", "print('outside the block')"],
              "The condition is false, so the block is skipped. The last line is not indented and runs in any case."),
         ]),
    dict(id="password", name="if and else: the password check", title="if and else: the password check", part=3, visual="password",
         concepts=["if", "else", "Flow Control Statements"],
         groups=[
             (["username = 'Mary'", "password = 'swordfish'"],
              "Two variables hold what the user typed. The program decides what to print from them."),
             (["if username == 'Mary':", "    print('Hello, Mary')", "    if password == 'swordfish':", "        print('Access granted.')",
               "    else:", "        print('Wrong password.')"],
              "An if can sit inside a block of another if. The else runs when the condition above it is false."),
         ]),
    dict(id="elif", name="elif: the ladder with one exit", title="elif: a ladder with one exit", part=3, visual="elif", layout="col",
         concepts=["elif", "Flow control statement"],
         groups=[
             (["name, age = 'Carol', 3000"],
              "Carol is 3000 years old. The ladder below asks about her name first and her age after that."),
             (["if name == 'Alice':", "    print('Hi, Alice.')", "elif age < 12:", "    print('You are not Alice, kiddo.')"],
              "Python tests the rungs from the top. The first true condition runs its block and the rest of the ladder is skipped."),
             (["elif age > 2000:", "    print('Alice is not an undead vampire.')", "elif age > 100:", "    print('You are not Alice, grannie.')"],
              "Each elif is tried only when every condition above it was false. Here age 3000 stops at the third rung."),
         ]),
    dict(id="elifOrder", name="Order of the elif rungs", title="elif: the order of the rungs matters", part=3, visual="elifOrder", layout="col",
         concepts=["elif", "else"],
         groups=[
             (["for age in (5, 50, 150, 3000):", "    if age < 12:", "        print(age, 'kiddo')"],
              "A loop tries four ages, one after the other. The first rung catches every child."),
             (["    elif age > 100:", "        print(age, 'grannie')", "    elif age > 2000:", "        print(age, 'vampire')"],
              "Every age above 2000 is also above 100, so 3000 is stopped at the grannie rung. The vampire rung can never run."),
             (["    else:", "        print(age, 'stranger')"],
              "The else catches what no rung has caught. Age 50 is neither a child nor above 100, so it is a stranger."),
         ]),
    dict(id="oppositeday", name="Short program: Opposite Day", title="A short program: Opposite Day", part=4, visual="oppositeday", layout="col",
         concepts=["A Short Program: Opposite Day", "Flow Control Statements"],
         groups=[
             (["opposite_day = True", "if opposite_day == True:", "    say_it = True", "else:", "    say_it = False"],
              "First the variable is set from the flag. On an Opposite Day it starts as True."),
             (["if opposite_day == True:", "    say_it = not say_it", "if say_it == True:", "    print('Today is Opposite Day.')", "else:",
               "    print('Today is not Opposite Day.')"],
              "On an Opposite Day the answer is flipped with not. The last if prints the answer."),
         ]),
    dict(id="capacity", name="Short program: Dishonest Capacity Calculator", title="A short program: the Dishonest Capacity Calculator", part=4, visual="capacity", layout="col",
         concepts=["A Short Program: Dishonest Capacity Calculator", "elif"],
         groups=[
             (["advertised = 10", "unit = 'TB'"],
              "A disk sold as 10 TB; the maker counts in tens."),
             (["if unit == 'TB' or unit == 'tb':", "    discrepancy = 10**12 / 2**40"],
              "A terabyte is 10 to the 12 bytes or 2 to the 40."),
             (["elif unit == 'GB' or unit == 'gb':", "    discrepancy = 10**9 / 2**30", "else:", "    discrepancy = 1"],
              "elif handles gigabytes; else keeps other units defined."),
             (["real = advertised * discrepancy", "print('Real capacity:', round(real, 2), unit)"],
              "Real capacity is the advertised size times the discrepancy."),
         ]),
    dict(id="condexpr", name="The conditional expression", title="One line: the conditional expression", part=5, visual="condexpr",
         concepts=["if", "else"],
         groups=[
             (["for n in (7, 10):", "    print(n, 'even' if n % 2 == 0 else 'odd')"],
              "A value if a condition else another value: it picks one of two values in a single expression."),
             (["print('adult' if 20 >= 18 else 1 / 0)"],
              "Only the chosen side is evaluated. The division by zero in the other side is never run."),
         ]),
    dict(id="match", name="match and case", title="match: a switch that matches patterns", part=5, visual="match", layout="col",
         concepts=["Flow Control Statements", "Flow control statement"],
         groups=[
             (["for status in (200, 403, 418):", "    match status:", "        case 200:", "            print(status, 'ok')"],
              "match compares a value with each case from the top. The first case fits only the number 200."),
             (["        case 401 | 403 | 404:", "            print(status, 'not allowed')", "        case _:", "            print(status, 'other')"],
              "A pipe joins alternatives into one case. The underscore matches anything, so it belongs at the end."),
         ]),
    dict(id="matchseq", name="match with sequences", title="match: sequences and captures", part=5, visual="matchseq", layout="col",
         concepts=["Flow Control Statements"],
         groups=[
             (["commands = [['go', 'north'], ['quit'], ['dance']]", "for command in commands:", "    match command:", "        case ['go', direction]:",
               "            print('going', direction)"],
              "A pattern can take a list apart. The name direction captures the second item of the list."),
             (["        case ['quit']:", "            print('bye')", "        case _:", "            print('unknown', command)"],
              "A list with one item fits the quit case. Anything else falls through to the underscore."),
         ]),
    dict(id="matchguard", name="match with a guard", title="match: guards", part=5, visual="matchguard", layout="col",
         concepts=["Flow Control Statements"],
         groups=[
             (["for point in ((3, 3), (3, 4)):", "    match point:", "        case (x, y) if x == y:", "            print('diagonal at', x)"],
              "A guard adds an if to a case. The first case fits only when both items of the pair are equal."),
             (["        case (x, y):", "            print('elsewhere', x, y)"],
              "Without the guard this case fits every pair, so it must stand after the guarded one."),
         ]),
    dict(id="walrus", name="The walrus operator", title="The walrus: test and keep in one step", part=5, visual="walrus",
         concepts=["if", "Boolean value"],
         groups=[
             (["names = ['Al', 'Alice', 'Bartholomew']", "for name in names:", "    if (size := len(name)) > 3:",
               "        print(name, 'has', size, 'letters')"],
              "The walrus := assigns a value and gives it back. Here size is stored and tested in the same condition."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
