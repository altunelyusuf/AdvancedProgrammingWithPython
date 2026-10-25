"""Chapter 1 deck examples, version 4.0.0: the code examples of the chapter 1 lecture deck (Python Basics).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained, uses only built-ins and prints what it shows (a script prints; the interactive shell
would echo each value by itself). No example waits for the keyboard: where the book calls input(), the example names
the text input() would have returned. A failing line sits in a two-line try/except, so the error text is part of the result.
Nothing here carries a result; deck_build_v4_0_0.py runs the code and takes every printed result from the run."""
__version__ = "4.0.0"

EXAMPLES = [
    dict(id="shell", name="The prompt as a calculator", title="The shell: type an expression, get a value", part=1, visual="shell",
         concepts=["Entering Expressions into the Interactive Shell", "Expression"],
         groups=[
             (["print(2 + 2)", "print('Py' + 'thon')"],
              "Python reads an expression, computes its value and shows it. 2 + 2 gives the number 4; 'Py' + 'thon' joins two pieces of text."),
             (["print(2 + 3 * 6)", "print(3 * (2 + 4))"],
              "An expression may hold several operators. Multiplication goes before addition, and parentheses go before everything."),
         ]),
    dict(id="types", name="Three data types", title="Data types: int, float and str", part=1, visual="types",
         concepts=["The Integer, Floating-Point, and String Data Types", "Data type"],
         groups=[
             (["print(type(7))", "print(type(3.5))", "print(type('Alice'))"],
              "type names the data type of a value: int for whole numbers, float for numbers with a fraction, str for text."),
             (["print(type(7 + 1))", "print(type(7 + 1.0))"],
              "A whole number plus a whole number stays an int. Mix in one float and the whole result becomes a float."),
         ]),
    dict(id="ints", name="Integers are exact", title="Integers never overflow", part=1, visual="ints",
         concepts=["The Integer, Floating-Point, and String Data Types"],
         groups=[
             (["print(7 + 1)", "print(2 ** 100)", "print(len(str(2 ** 100)))"],
              "A Python integer has no size limit. 2 ** 100 is written out in full, all 31 digits, and it is exact."),
             (["print(int('42') + 1)", "print(int(4.7))"],
              "int reads text as a whole number. Given a float it cuts the fraction away; it does not round."),
         ]),
    dict(id="floats", name="Floats are approximate", title="Floats are honest about being approximate", part=1, visual="floats",
         concepts=["The Integer, Floating-Point, and String Data Types"],
         groups=[
             (["print(0.1 + 0.2)", "print(round(0.1 + 0.2, 2))", "print(0.1 + 0.2 == 0.3)"],
              "A float is stored in binary, so 0.1 and 0.2 are only close. round shows a tidy number, but == still says they differ."),
             (["print(6 / 3)", "print(type(6 / 3))", "print(4 * 3.75 - 1)"],
              "Division with / always gives a float, even when it divides evenly. A float in the mix makes the result a float."),
         ]),
    dict(id="strings", name="Strings are text", title="Strings: text between quotes", part=1, visual="strings",
         concepts=["The Integer, Floating-Point, and String Data Types", "Data type"],
         groups=[
             (["print('Hello, world!')", "print(len('Hello, world!'))"],
              "A string is text between quotes. len counts every character, and spaces and punctuation count too."),
             (["print('7' == 7)", "print(type('7'), type(7))"],
              "The text '7' and the number 7 look alike but are different values of different types, so they are not equal."),
         ]),
    dict(id="ops", name="Seven arithmetic operators", title="Seven operators for numbers", part=2, visual="ops",
         concepts=["Expression"],
         groups=[
             (["print(5 + 2)", "print(5 - 2)", "print(5 * 2)", "print(5 / 2)"],
              "Plus, minus and times work as in school. The slash divides and always gives a float."),
             (["print(5 // 2)", "print(5 % 2)", "print(5 ** 2)"],
              "Two slashes give the whole part of the division, the percent sign gives the remainder, and two stars raise to a power."),
         ]),
    dict(id="prec", name="Operator precedence", title="Who goes first: operator precedence", part=2, visual="prec",
         concepts=["Operator precedence"],
         groups=[
             (["print(2 + 3 * 6)", "print((2 + 3) * 6)"],
              "Multiplication binds tighter than addition, so 2 + 3 * 6 is 20. Parentheses override the order and give 30."),
             (["print(-3 ** 2)", "print((-3) ** 2)", "print(8 / 2 * 3)"],
              "The power binds tighter than the minus sign, so -3 ** 2 is -9. Equal operators run from left to right."),
         ]),
    dict(id="intdiv", name="Quotient and remainder", title="Division three ways: quotient and remainder", part=2, visual="intdiv",
         concepts=["Expression"],
         groups=[
             (["print(23 // 7)", "print(23 % 7)", "print(23 // 7 * 7 + 23 % 7)"],
              "23 candies in boxes of 7 fill 3 boxes and leave 2 over. Quotient times divisor plus remainder gives 23 back."),
             (["print(-7 // 2)", "print(23 / 7)"],
              "Floor division rounds down, so -7 // 2 is -4, not -3. True division keeps the fraction and gives a float."),
         ]),
    dict(id="concat", name="Joining strings", title="String concatenation: + joins text", part=2, visual="concat",
         concepts=["String Concatenation and Replication", "String concatenation"],
         groups=[
             (["print('Alice' + 'Bob')", "print('Hello' + ' ' + 'world')"],
              "Plus between two strings glues them together. No space is added, so a space has to be part of one string."),
             (["try: print('Alice' + 42)", "except TypeError as e: print('TypeError:', e)"],
              "Plus does not glue text to a number. Python stops with a TypeError that names both types."),
             (["print('Alice' + str(42))"],
              "str turns the number into text first, and then the join works."),
         ]),
    dict(id="repl", name="Repeating strings", title="String replication: * repeats text", part=2, visual="repl",
         concepts=["String Concatenation and Replication"],
         groups=[
             (["print('Alice' * 3)", "print(3 * 'ab')", "print(repr('ab' * 0))"],
              "Star between a string and a whole number repeats the string. The order does not matter, and zero copies give an empty string."),
             (["try: print('Alice' * 2.5)", "except TypeError as e: print('TypeError:', e)"],
              "The count must be an integer. A float such as 2.5 raises a TypeError."),
         ]),
    dict(id="var", name="Variables", title="Variables: names that remember", part=3, visual="var",
         concepts=["Storing Values in Variables", "Variable"],
         groups=[
             (["spam = 42", "print(spam)", "spam = spam + 1", "print(spam)"],
              "The equals sign stores a value under a name. Assigning again gives the name a new value; the old value is replaced."),
             (["try: print(Spam)", "except NameError as e: print('NameError:', e)"],
              "Names are case-sensitive. Spam was never assigned, so Python reports a NameError."),
         ]),
    dict(id="print", name="print() and its options", title="print: the function that shows", part=3, visual="print",
         concepts=["print"],
         groups=[
             (["print('Hello,', 'world!')", "print('Hello,', 'world!', sep='-', end=' <end>\\n')"],
              "print separates its items with a space and ends the line. The options sep and end change the separator and the ending."),
             (["print()", "print('the line above is empty')"],
              "print with nothing in the parentheses writes an empty line."),
         ]),
    dict(id="conv", name="str, int, float and len", title="Conversions and len: built-in functions", part=3, visual="conv",
         concepts=["str", "int", "float", "len"],
         groups=[
             (["print(str(29))", "print(int('42'))", "print(float('3.5'))", "print(int(4.7))"],
              "str makes text, int makes a whole number and float makes a number with a fraction. Each one converts its argument."),
             (["print(len('hello'))", "print(len(str(12345)))"],
              "len counts characters. A number has no length, so str turns 12345 into text first: five characters."),
         ]),
    dict(id="errors", name="Errors that teach", title="Errors are answers too", part=3, visual="errors",
         concepts=["int", "len"],
         groups=[
             (["try: print(int('4.2'))", "except ValueError as e: print('ValueError:', e)"],
              "The type is right but the content is wrong: int cannot read the text 4.2 as a whole number. That is a ValueError."),
             (["try: print(len(12345))", "except TypeError as e: print('TypeError:', e)"],
              "The type itself is wrong: a number has no length. That is a TypeError."),
         ]),
    dict(id="input", name="input() gives text", title="input always returns text", part=3, visual="input",
         concepts=["Input as text", "input"],
         groups=[
             (["typed = '20'  # the text input() would return", "print(type(typed).__name__)"],
              "Whatever a person types, input hands back a string. This example names the text directly so it needs no keyboard."),
             (["print(typed + '1')", "print(int(typed) + 1)"],
              "Plus on the text glues characters: 201. Convert with int first and plus adds: 21."),
         ]),
    dict(id="module", name="import opens a module", title="Modules: import opens a toolbox", part=3, visual="module",
         concepts=[],
         groups=[
             (["import math", "print(type(math).__name__)"],
              "import binds a module to a name. A module is a toolbox of ready-made functions and values."),
             (["print(math.sqrt(16))", "print(math.pi)"],
              "A dot reaches inside the module: sqrt is a function, pi is a value. sqrt always returns a float."),
         ]),
    dict(id="first", name="Your first program", title="Your first program", part=4, visual="first", layout="left",
         concepts=["Your First Program", "print", "input", "len"],
         groups=[
             (["print('Hello, world!')", "print('What is your name?')"],
              "Two print calls greet the user and ask a question."),
             (["my_name = 'Ayse'  # the text input() would return", "print('It is good to meet you, ' + my_name)",
               "print('The length of your name is:')", "print(len(my_name))"],
              "A variable keeps the name. Concatenation builds the greeting and len measures the name."),
             (["my_age = '20'  # input() returns text", "next_age = int(my_age) + 1", "print('You will be ' + str(next_age) + ' next year.')"],
              "int turns the age text into a number so that plus can add one. str turns the result back into text for the join."),
         ]),
    dict(id="dissect", name="Dissecting the program", title="Dissecting the program: join or fill in", part=4, visual="dissect", layout="below",
         concepts=["Dissecting the Program", "str", "String concatenation"],
         groups=[
             (["name = 'Alice'", "age = 20"],
              "Two variables hold the pieces of the message."),
             (["print('Hello, ' + name + '! You are ' + str(age) + '.')", "print(f'Hello, {name}! You are {age}.')"],
              "Both lines print the same sentence. The first joins five pieces and needs str. The f-string fills named slots with values."),
         ]),
    dict(id="binary", name="Binary numbers", title="How computers store numbers: binary", part=4, visual="binary",
         concepts=["How Computers Store Data with Binary Numbers"],
         groups=[
             (["print(bin(5))", "print(int('101', 2))", "print(2 ** 8)"],
              "bin shows a number as binary digits. int with base 2 reads them back. Eight binary digits, one byte, hold 2 ** 8 = 256 values."),
             (["print(format(5, '08b'))", "print(format(255, '08b'))"],
              "format with 08b writes a number as exactly eight binary digits, padded with zeros on the left."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
