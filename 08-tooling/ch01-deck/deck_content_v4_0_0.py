"""Chapter 1 deck content, version 4.0.0: the words of the deck (parts, analogies, stories, notes, take-aways, resources).
Every concept label of the chapter research (sen0414_ch01_research_v1_1_0.ttl, the PrimarySourceConcept resources) has its
everyday analogy here, under the research's own label, so the deck check can find it. Stories follow 5N1K with a dated,
sourced account, a picture whose licence is recorded in 03-materials/ch01/assets/ASSETS_PROVENANCE_v1_1_0.md and a live link.
Facts of the stories: Python's origin (Wikipedia 'Guido van Rossum' and the history of Python, opened 2026-10-25), the first
'hello, world' (Wikipedia '"Hello, World!" program', citing Kernighan 1972 and Kernighan and Ritchie 1978), Leibniz's binary
arithmetic (historyofinformation.com, entry 395); the earlier stories file is 08-tooling/sen0414_ch01_stories_v1_0_0.py."""
__version__ = "4.0.0"

# ---- the four parts: (title, subtitle, [(concept pill of at most four words, one line of meaning of at least five words)])
PARTS = {
    1: ("Part 1: Values and types", "What the prompt computes with, and how Python labels it", [
        ("Expression", "A piece of code that Python turns into one value."),
        ("Data type", "The label that says what a value is and what it can do."),
        ("Integer", "A whole number, exact however large it grows."),
        ("Float and string", "A number with a fraction, and text between quotes."),
    ]),
    2: ("Part 2: Operations", "Combining values: arithmetic, the order of work, and two string operators", [
        ("Operators", "Symbols such as plus, minus and star that combine values."),
        ("Precedence", "The order in which operators run; parentheses go first."),
        ("Concatenation", "Plus joins two strings into one longer string."),
        ("Replication", "Star repeats a string a whole number of times."),
    ]),
    3: ("Part 3: Names and functions", "Remembering values, and the toolbox that comes with Python", [
        ("Variable", "A name that refers to a value and can be reassigned."),
        ("print and input", "One shows text on the screen, the other reads typed text."),
        ("str, int, float", "Built-in functions that convert one kind of value into another."),
        ("len", "Counts the characters of a string."),
    ]),
    4: ("Part 4: A first program", "Putting the pieces together, taking it apart, and how bits hold numbers", [
        ("Hello, world", "The smallest program that shows a visible result."),
        ("Dissecting", "Reading a program line by line and naming each part."),
        ("f-string", "Fills named slots with values instead of joining pieces."),
        ("Binary", "Numbers written with only the digits 0 and 1."),
    ]),
}

# ---- everyday analogies, grouped on the analogy slides: (slide id, title, headline analogy, [(research label, everyday picture)])
ANALOGIES = [
    ("A1", "Everyday pictures: values and types", "The shell is a pocket calculator with a screen: you type a sum and the answer appears at once.", [
        ("Entering Expressions into the Interactive Shell", "A pocket calculator with a screen: type a sum, read the answer, type the next one."),
        ("Expression", "A recipe line: ingredients and steps that end in one finished dish, the value."),
        ("The Integer, Floating-Point, and String Data Types", "Three kinds of container: crates for whole items, jugs for amounts with a fraction, signs for words."),
        ("Data type", "The label on a container: it says what may be put in and what may be done with it."),
    ]),
    ("A2", "Everyday pictures: operators", "An operator is a verb between two values, and precedence is the order of work in a kitchen: chop before you stir.", [
        ("Operator precedence", "The kitchen rule 'chop first, then stir'; parentheses are a note saying 'do this one first'."),
        ("+", "A scale pan that adds weights, or glue between two paper strips."),
        ("-", "Taking coins out of a purse."),
        ("*", "Stamping the same picture again and again."),
        ("/", "Sharing a pizza fairly: every slice may be a fraction."),
        ("//", "Counting how many full boxes you can fill."),
        ("%", "The crumbs left over after the boxes are full."),
        ("**", "Folding a sheet of paper: each fold doubles the thickness."),
    ]),
    ("A3", "Everyday pictures: operations on text", "Concatenation is glue and replication is a photocopier, both working on paper strips of text.", [
        ("String concatenation", "Gluing two paper strips end to end to make a longer strip."),
        ("String Concatenation and Replication", "A glue stick and a photocopier: join two strips, or copy one strip several times."),
        ("str", "A label maker that prints any value as a text label."),
    ]),
    ("A4", "Everyday pictures: names", "A variable is a labelled jar: the label is the name, the contents are the value.", [
        ("Storing Values in Variables", "Putting something into a jar and writing a label on it."),
        ("Variable", "The label on the jar: read the jar through its label, or swap the contents."),
        ("print", "A loudspeaker: whatever you hand it is announced to the room."),
        ("input", "A suggestion box: the person writes on paper and drops it in."),
        ("Input as text", "Everything in the suggestion box is paper: even a number arrives as written characters."),
    ]),
    ("A5", "Everyday pictures: functions and modules", "A built-in function is a machine with a slot for the input and a slot for the result.", [
        ("len", "A ruler laid along the text: it tells how many characters, not what they mean."),
        ("int", "A machine that reads text as a whole number and trims any fraction away."),
        ("float", "A machine that turns text or a whole number into a number with a decimal point."),
        ("Modules (import)", "A toolbox fetched from the shelf: import carries it to your desk."),
    ]),
    ("A6", "Everyday pictures: a program and its bits", "A program is a recipe: steps in order, ingredients kept in labelled jars.", [
        ("Your First Program", "A recipe followed line by line: greet, ask, answer."),
        ("Dissecting the Program", "Taking a clock apart: each gear does one small job, and together they tell the time."),
        ("How Computers Store Data with Binary Numbers", "A row of light switches: each is on or off, and the pattern of switches is the number."),
    ]),
]

# ---- stories (5N1K): each box is one label and at most 30 words
STORIES = {
    "guido": dict(title="Story: a Christmas hobby named after a comedy troupe", img="photo_guido_van_rossum.jpg",
                  credit="Guido van Rossum, 2014. Photo: Daniel Stroud, CC BY-SA 4.0, Wikimedia Commons.",
                  who="Guido van Rossum, a programmer at the Centrum Wiskunde & Informatica (CWI), working on the Amoeba project.",
                  what="A hobby scripting language, a descendant of ABC, meant to be more readable than shell scripts.",
                  when="December 1989, in the Christmas week when the office was closed; version 0.9.0 followed in February 1991.",
                  where="At CWI in Amsterdam; the source code was posted to the alt.sources Usenet group.",
                  why="He wanted a language that is easy to read and to program, and he had a week without work.",
                  how="He named it after the British comedy troupe Monty Python, not after the snake.",
                  short="Story: Guido van Rossum and Python", link="https://en.wikipedia.org/wiki/Guido_van_Rossum", linktext="Guido van Rossum (Wikipedia)"),
    "kernighan": dict(title="Story: where hello, world began, in 1972", img="photo_brian_kernighan.jpg",
                      credit="Brian Kernighan, 2012, at Bell Labs. Photo: Ben Lowe, CC BY 2.0, Wikimedia Commons.",
                      who="Brian Kernighan, a researcher at Bell Laboratories.",
                      what="The first known program to put the words hello and world together, written as a teaching example.",
                      when="1972, in A Tutorial Introduction to the Language B; the 1978 book The C Programming Language made it famous.",
                      where="Bell Laboratories; page 6 of the 1978 book, published by Prentice Hall.",
                      why="A beginner needs a first program that does one visible thing: print a greeting.",
                      how="B held only four characters per constant, so the text sat in three variables; Python needs one line.",
                      short="Story: Brian Kernighan, hello, world", link="https://en.wikipedia.org/wiki/%22Hello,_World!%22_program", linktext="The Hello, World! program (Wikipedia)"),
    "leibniz": dict(title="Story: Leibniz wrote every number with only 0 and 1", img="photo_gottfried_leibniz.jpg",
                    credit="Gottfried Wilhelm Leibniz, painting by Christoph Bernhard Francke, before 1729, Herzog Anton Ulrich Museum. Public domain, Wikimedia Commons.",
                    who="Gottfried Wilhelm Leibniz, philosopher and mathematician; the Jesuit Joachim Bouvet wrote to him from China.",
                    what="Binary arithmetic: every number written with the two digits 0 and 1, described in Explication de l'arithmétique binaire.",
                    when="First notes on 15 March 1679; Bouvet's letter arrived on 1 April 1703; the paper was printed in 1705.",
                    where="He sent the paper to the Académie Royale des Sciences in Paris; Bouvet's letter came from Peking.",
                    why="Bouvet saw that the hexagrams of the Chinese I Ching are binary numbers; Leibniz saw order in them.",
                    how="Every number is a sum of powers of two: 5 is 4 plus 1, written 101. Computers store numbers this way.",
                    short="Story: Leibniz and binary numbers", link="https://historyofinformation.com/detail.php?id=395", linktext="Leibniz and the binary system (historyofinformation.com)"),
}
STORY_NOTES = {
    "guido": "Guido van Rossum began Python in the Christmas week of 1989 at CWI in Amsterdam. The name comes from Monty Python. Ask students which of today's examples they would have written in a language without this readability.",
    "kernighan": "The first hello, world was in a 1972 tutorial for the language B. In B the text needed three variables; in Python it is one line. Ask what a first program proves: that writing, running and seeing output all work.",
    "leibniz": "Leibniz described binary arithmetic in 1679 and in a paper for the Paris Academy in 1703. Bouvet's letter from Peking showed the I Ching hexagrams as binary numbers. Ask: why do computers prefer two digits?",
}

# ---- speaker notes, short (at most 60 words each)
NOTES = {
    "title": "Welcome. This chapter is the prompt, the values it computes with, the operators that combine them, the names that remember them, and a first program. Every code slide shows the code, a plain explanation, and what the run printed as a table, chart or drawing.",
    "route": "Four parts: values and types, operations, names and functions, and a first program. Each range is a run of slides you can jump to. The chapter-code tab of the page holds the same examples in the same order.",
    "questions": "Three questions to carry through the chapter. Which operations can raise an error, and which? Which results can surprise a student? And what has changed in current Python since the book?",
    "divider1": "Part one. The shell evaluates an expression and prints its value. Every value has a data type: integer, float or string. Notice which results surprise you.",
    "divider2": "Part two. Operators combine values. Precedence decides who goes first, and parentheses override it. Plus and star also work on strings, with a different meaning.",
    "divider3": "Part three. A variable is a name for a value. Print shows, input reads, and str, int, float and len convert and measure. Errors are answers too.",
    "divider4": "Part four. A first program uses everything so far. Then we take it apart line by line, and finish with the binary digits behind every number.",
    "A1": "A calculator with a screen is the shell. An expression is a recipe line that ends in one value. A data type is the label on a container. Ask students to add their own everyday picture.",
    "A2": "Operators are verbs between values. Precedence is the order of work: chop before you stir. Go through the eight pictures and ask which one students remember best.",
    "A3": "Concatenation glues strips of text, replication photocopies them. Str is the label maker that turns any value into text. Keep the pictures; the code comes next.",
    "A4": "A variable is a labelled jar. Print is the loudspeaker, input is the suggestion box. Everything in the box is paper, so even a number arrives as text.",
    "A5": "Len is a ruler for text. Int and float are machines with a slot in and a slot out. Ask which machine rejects the input and why.",
    "A6": "A program is a recipe. Dissecting it is taking a clock apart. Binary is a row of light switches. Each picture comes back on the slide that follows.",
    "shell": "The shell is a calculator that answers. In a program you write print yourself. Ask students to predict 2 + 3 * 6 before the run, and why it is not 30.",
    "types": "Type names the data type of any value. A whole number plus a float gives a float. Ask: what type does 7 + 1.0 have, and why?",
    "ints": "Python integers never overflow. 2 to the power 100 has 31 digits and is exact. Int turns text into a number, and cuts a float without rounding.",
    "floats": "Zero point one plus zero point two is not exactly zero point three. Floats are binary fractions, so many decimals do not fit. Division with a slash always gives a float.",
    "strings": "A string is text between quotes. Len counts characters. The text seven and the number seven are different values; Python never converts between them silently.",
    "ops": "Seven operators: plus, minus, times, divide, floor divide, remainder, power. The slash always gives a float. The double slash and the percent sign work as a pair.",
    "prec": "The power goes first, then times and divide, then plus and minus. Parentheses override. Minus three to the power two is minus nine, because the power binds tighter. Predict, then run.",
    "intdiv": "Twenty-three candies in boxes of seven: three boxes and two left. Floor division gives the boxes, percent gives the rest. Floor division rounds down, so minus seven by two is minus four.",
    "concat": "Plus joins strings and adds no space. Joining text to a number is a TypeError, because Python does not convert silently. Str fixes it. Errors are answers: read the message.",
    "repl": "Star repeats a string. The count must be a whole number; a float raises a TypeError. Zero copies give the empty string. The chart shows how long each result is.",
    "var": "An assignment gives a name to a value. Assign again and the name refers to a new value. Names are case-sensitive: Spam was never assigned, so Python raises a NameError.",
    "print": "Print takes any number of items. The options sep and end change the separator and the ending. Print with nothing in the parentheses writes an empty line.",
    "conv": "Str, int and float convert. Len counts characters; a number has no length, so convert it to text first. The table shows input, function, result and type.",
    "errors": "A ValueError means the type is right but the content is wrong. A TypeError means the type itself does not fit the operation. Reading the error name tells you where to look.",
    "module": "Import brings in a toolbox. The dot reaches inside it for a function, sqrt, or a value, pi. Standard library modules are free and always installed.",
    "input": "Input always returns text, even when the person types a number. Plus on text glues, plus on numbers adds. Convert with int before you calculate.",
    "first": "The first program greets, asks, measures and calculates. Because the page has no keyboard, the example names the text input would return. Trace it line by line in the table.",
    "dissect": "Two ways to build the same sentence: join five pieces with plus and str, or fill slots in an f-string. The f-string is shorter and needs no str. Which would you rather read?",
    "binary": "Bin shows binary digits, int with base 2 reads them. Eight binary digits make a byte and hold 256 values. Each place is a power of two; the chart shows which places are on for the number five.",
    "current": "Python moves on. The shell and its error messages improved in 3.13. The free-threaded build is experimental. F-strings have a formal grammar. Check each row against its source.",
    "summary": "Five sentences to keep. The chart counts the code examples of each part. Everything is on the chapter page, in the same order.",
    "practice": "Four drills. Predict first, then run on the page. Ask students to explain each answer in one sentence.",
    "resources": "Start with the book chapter and the Python tutorial. The stories link to first-hand sources. Choose one link and one video and read or watch it before the next class.",
}

TAKEAWAY = {
    "shell": "The shell evaluates an expression and prints its value.", "types": "type() names the data type: int, float or str.",
    "ints": "Integers are exact, however big.", "floats": "Floats are binary fractions; 0.1 + 0.2 is not 0.3.",
    "strings": "'7' is text and 7 is a number: different values.", "ops": "Seven operators; / always gives a float.",
    "prec": "Power first, then * and /, then + and -; parentheses win.", "intdiv": "// is the whole part, % is the rest.",
    "concat": "+ joins strings; mixing in a number is a TypeError.", "repl": "* repeats a string; the count is a whole number.",
    "var": "A name refers to a value; assigning again changes it.", "print": "sep and end change what print writes between and after.",
    "conv": "str, int and float convert; len counts characters.", "errors": "ValueError: wrong content. TypeError: wrong type.",
    "input": "input() returns text; convert before you calculate.", "module": "import brings a toolbox; a dot reaches inside it.", "first": "Greet, ask, measure, calculate: nine lines, four built-in functions.",
    "dissect": "Join pieces with +, or fill slots with an f-string.", "binary": "Every number is a sum of powers of two.",
}

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 1", "https://automatetheboringstuff.com/3e/chapter1.html", "automatetheboringstuff.com"),
    ("The Python Tutorial: an informal introduction", "https://docs.python.org/3/tutorial/introduction.html", "docs.python.org"),
    ("Floating-point arithmetic: issues and limitations", "https://docs.python.org/3/tutorial/floatingpoint.html", "docs.python.org"),
    ("Built-in functions, all of them", "https://docs.python.org/3/library/functions.html", "docs.python.org"),
    ("Built-in types", "https://docs.python.org/3/library/stdtypes.html", "docs.python.org"),
    ("PEP 8: the style guide", "https://peps.python.org/pep-0008/", "peps.python.org"),
    ("PEP 20: the Zen of Python", "https://peps.python.org/pep-0020/", "peps.python.org"),
    ("PEP 701: f-strings get a formal grammar", "https://peps.python.org/pep-0701/", "peps.python.org"),
    ("PEP 703: making the GIL optional", "https://peps.python.org/pep-0703/", "peps.python.org"),
    ("What's new in Python 3.14", "https://docs.python.org/3/whatsnew/3.14.html", "docs.python.org"),
    ("Status of Python versions", "https://devguide.python.org/versions/", "devguide.python.org"),
    ("uv: a fast Python package manager", "https://docs.astral.sh/uv/", "docs.astral.sh"),
    ("Video: The Story of Python, by Guido van Rossum", "https://www.youtube.com/watch?v=J0Aq44Pze-w", "youtube.com"),
    ("Leibniz and the binary system", "https://historyofinformation.com/detail.php?id=395", "historyofinformation.com"),
]
