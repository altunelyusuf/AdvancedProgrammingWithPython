"""Chapter 8 deck examples, version 2.0.0: the code examples of the chapter 8 lecture deck (Strings and Text Editing).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every statement is ONE line (no continuation lines), so the prompt convention is unambiguous. Every example is
self-contained: it defines what it uses. Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes
every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    dict(id="quotes", name="Quotes and apostrophes", title="Two kinds of quotes", part=1, visual="quotes",
         concepts=["String literal", "Double Quotes"],
         groups=[
             (["a = \"Alice's cat\"", "b = 'Bob\\'s cat'"],
              "Double quotes let an apostrophe sit inside the text. In single quotes a backslash escapes it."),
             (["print(a, len(a))", "print(b, len(b))"],
              "Both strings hold a plain apostrophe. The backslash is not stored, so lengths count real characters only."),
             (["print(type(b'a').__name__, type(r'a').__name__)"],
              "A b prefix builds bytes, not text. An r prefix still builds an ordinary str."),
         ]),
    dict(id="escapes", name="Escape sequences", title="Escape sequences", part=1, visual="escapes",
         concepts=["Escape Sequences"],
         groups=[
             (["print('a\\tb', len('a\\tb'))", "print('line1\\nline2'.split('\\n'))"],
              "A tab and a newline each count as one character. Splitting on the newline cuts the text into two lines."),
             (["print(len('\\\\'), len('\\''), len('\\\"'))"],
              "An escaped backslash or quote is also one character. The backslash only tells Python what comes next."),
         ]),
    dict(id="raw_multiline", name="Raw and multiline strings", title="Raw strings and triple quotes", part=1, visual="raw",
         concepts=["Raw Strings", "Multiline Strings"],
         groups=[
             (["path = r'C:\\Users\\Alice\\Desktop'", "print(path, len(path))", "print(len(r'\\n'), len('\\n'))"],
              "A raw string keeps every backslash as typed. So r'\\n' has two characters, while '\\n' has one."),
             (["note = '''She said \"it's fine\"'''", "print(note)"],
              "Triple quotes may hold both kinds of quote, and real line breaks too. No escapes are needed inside."),
         ]),
    dict(id="index", name="Index into a string", title="Indexes: a number for every character", part=1, visual="index",
         concepts=["Index", "Indexes and Slices"],
         groups=[
             (["greeting = 'Hello, world!'", "print(greeting[0], greeting[4], greeting[-1])"],
              "Counting starts at 0 on the left. Negative numbers count back from the end, so -1 is the last character."),
             (["print(len(greeting), greeting[len(greeting) - 1])"],
              "The last index is the length minus one. Index -1 reaches the same character without any arithmetic."),
         ]),
    dict(id="slice", name="Slices of a string", title="Slices: cutting out a piece", part=1, visual="slice",
         concepts=["Slice", "Indexes and Slices"],
         groups=[
             (["greeting = 'Hello, world!'", "print(greeting[0:5], greeting[7:-1])"],
              "A slice takes the characters from start up to, but not including, stop."),
             (["print(greeting[:5], greeting[7:], greeting[::-1])"],
              "Leave out start or stop to run to an edge. A step of -1 walks backwards and reverses the text."),
         ]),
    dict(id="in_immutable", name="in, not in and immutability", title="in, not in and strings that never change", part=1, visual="in",
         concepts=["The in and not in Operators"],
         groups=[
             (["name = 'Zophie a cat'", "print(name[0:7] + 'the' + name[8:12])"],
              "A string cannot be changed in place. To edit it, build a new string from slices of the old one."),
             (["print('Hello' in 'Hello, World', 'HELLO' in 'Hello, World')", "print('' in 'spam', 'cats' not in 'cats and dogs')"],
              "The in operator asks whether one text sits inside another, and it is case sensitive. The empty string is inside every string."),
         ]),
    dict(id="fstring", name="F-strings", title="F-strings: text with holes", part=2, visual="fstring",
         concepts=["F-Strings", "F-string"],
         groups=[
             (["name = 'Al'", "age = 4000"],
              "Two ordinary variables. An f-string will reach into them by name."),
             (["print(f'My name is {name}. I am {age} years old.')", "print(f'In ten years I will be {age + 10}. {{name}}')"],
              "Anything inside braces is evaluated and pasted in, even a sum. Doubled braces print one literal brace."),
         ]),
    dict(id="fspec", name="Format specifications", title="Format specifications after the colon", part=2, visual="fspec",
         concepts=["F-Strings"],
         groups=[
             (["print(f'{3.14159:.2f}|{42:>6}|{42:^6}|')", "print(f'{1234567:,}|{255:#x}')"],
              "The text after a colon says how to show the value: decimals, width, alignment, separators, hexadecimal."),
             (["n = 7", "print(f'{n=}', f'{n + 1 = }')"],
              "An equals sign prints the expression and its value. It is the quickest way to debug a value."),
         ]),
    dict(id="older", name="Older formatting styles", title="Older styles: %s, format() and plus", part=2, visual="older",
         concepts=["F-String Alternatives: %s and format()", "format"],
         groups=[
             (["name = 'Al'", "age = 4000"],
              "The same two variables, now used by the older formatting styles."),
             (["print('My name is %s. I am %s years old.' % (name, age))", "print('{1} years ago, {0} was born.'.format(name, age))"],
              "A percent s slot takes values in order. A numbered brace slot takes values by position, in any order."),
             (["print('Py' 'thon', 3 * 'un' + 'ium')"],
              "Neighbouring literals join. The star repeats a string, and plus joins two."),
         ]),
    dict(id="case", name="Changing the case", title="Changing the case", part=3, visual="case",
         concepts=["Changing the Case", "upper", "lower"],
         groups=[
             (["s = 'Hello, world!'", "print(s.upper())", "print(s.lower())"],
              "upper and lower never change s. Each returns a new string, so you must keep or print the result."),
             (["print('great' == 'GREat'.lower())", "print('stra\u00dfe'.casefold() == 'strasse')"],
              "Compare after lowering to ignore case. casefold goes further: the German sharp s equals ss."),
         ]),
    dict(id="chars", name="Testing the characters", title="Testing what a string is made of", part=3, visual="chars",
         concepts=["Checking String Characteristics", "isalpha", "isalnum", "isdecimal", "isspace"],
         groups=[
             (["words = ['hello', 'Hello', 'abc123', '123', ' ']"],
              "Five sample strings: letters, a capital, letters with digits, digits only and a single space."),
             (["print([w.isalpha() for w in words])", "print([w.isalnum() for w in words])"],
              "isalpha wants letters only. isalnum also accepts digits. Each test returns True or False for the whole string."),
             (["print([w.isdecimal() for w in words])", "print([w.isspace() for w in words])"],
              "isdecimal wants digits only. isspace wants nothing but blanks, tabs and line breaks."),
         ]),
    dict(id="casetests", name="Testing the case", title="Testing upper, lower and title case", part=3, visual="casetests",
         concepts=["isupper", "islower", "istitle"],
         groups=[
             (["words = ['hello', 'Hello', 'HELLO', 'Hello World', '123']"],
              "Five samples. Digits have no case at all, which matters for the tests below."),
             (["print([w.isupper() for w in words])", "print([w.islower() for w in words])", "print([w.istitle() for w in words])"],
              "isupper and islower need at least one letter and all letters in that case. istitle wants every word capitalised."),
         ]),
    dict(id="affixes", name="Start, end and affixes", title="Start, end and affixes", part=3, visual="affixes",
         concepts=["Checking the Start or End of a String", "startswith", "endswith"],
         groups=[
             (["print('Hello, world!'.startswith('Hello'))", "print('notes.txt'.endswith(('.py', '.txt')))"],
              "startswith and endswith test one end of a string. Give endswith a tuple to accept several endings."),
             (["print('report.txt'.removesuffix('.txt'))", "print('test_a.py'.removeprefix('test_'))"],
              "removesuffix and removeprefix cut off exactly that text, once. strip would remove a set of characters."),
         ]),
    dict(id="joinsplit", name="Join and split", title="Joining and splitting", part=3, visual="joinsplit",
         concepts=["Joining and Splitting Strings", "join", "split"],
         groups=[
             (["print(', '.join(['cats', 'rats', 'bats']))"],
              "join glues a list of strings with the string it is called on between them."),
             (["print('My name is Simon'.split('m'))", "print('My name is Simon'.split())"],
              "split cuts at a chosen text. With no argument it cuts at every run of whitespace."),
             (["print('one\\r\\ntwo\\nthree'.splitlines())", "print('Monty Python'.partition(' '))"],
              "splitlines handles every kind of line break. partition cuts once and keeps the separator."),
         ]),
    dict(id="justify", name="Justify and centre", title="Justifying and centring text", part=3, visual="justify",
         concepts=["Justifying and Centering Text", "rjust", "ljust", "center"],
         groups=[
             (["print('Hello'.rjust(10) + '|')", "print('Hello'.ljust(10, '-') + '|')"],
              "rjust pads on the left, ljust on the right, up to the width you give. An optional fill character replaces the spaces."),
             (["print('Hello'.center(20, '=') + '|')"],
              "center pads both sides. The bar after each result makes the trailing padding visible."),
         ]),
    dict(id="strip", name="Removing whitespace", title="Removing whitespace", part=3, visual="strip",
         concepts=["Removing Whitespace", "strip", "lstrip", "rstrip"],
         groups=[
             (["s = '    Hello, World    '", "print(len(s), len(s.strip()), len(s.lstrip()), len(s.rstrip()))"],
              "strip removes blanks at both ends, lstrip on the left only, rstrip on the right only. The lengths show what was cut."),
             (["print('SpamSpamBaconSpamEggsSpamSpam'.strip('ampS'))"],
              "Given an argument, strip removes any of those characters, in any order, from both ends. It is a set, not a word."),
         ]),
    dict(id="search", name="Find, count and replace", title="Finding, counting and replacing", part=3, visual="search",
         concepts=["Useful String Methods"],
         groups=[
             (["s = 'spam eggs spam'", "print(s.find('spam'), s.find('spam', 1), s.count('spam'))"],
              "find gives the index of the first match, or -1. A start argument skips ahead. count tallies the matches."),
             (["print(s.replace('spam', 'ham', 1))"],
              "replace returns a new string. The last argument limits how many matches change."),
         ]),
    dict(id="codepoints", name="Code points: ord and chr", title="Code points: ord() and chr()", part=4, visual="codepoints",
         concepts=["Numeric Code Points of Characters", "Unicode code point", "ord()", "chr()"],
         groups=[
             (["print(ord('A'), chr(65), chr(ord('A') + 1))"],
              "ord turns a character into its number. chr turns a number back into a character."),
             (["print([ord(c) for c in 'Hello'])"],
              "Every character has a number. Capitals and small letters have different numbers, a fixed distance apart."),
         ]),
    dict(id="encoding", name="Characters versus bytes", title="Characters are not bytes", part=4, visual="encoding",
         concepts=["Encoding"],
         groups=[
             (["print('caf\u00e9'.encode('utf-8'))", "print(len('caf\u00e9'), len('caf\u00e9'.encode('utf-8')))"],
              "Four characters become five bytes in UTF-8, because the accented letter takes two bytes."),
             (["print([len(c.encode('utf-8')) for c in 'a\u20ac\u00e9'])", "print('caf\u00e9'.encode('ascii', errors='replace'))"],
              "UTF-8 spends one to four bytes per character. ASCII cannot hold the accent, so errors=replace puts a question mark."),
         ]),
    dict(id="book_rjust", name="The book's rjust lines, re-run", title="Re-running the book's rjust lines", part=4, visual="bookcheck",
         concepts=["rjust"],
         groups=[
             (["print(len('Hello'.rjust(20)) - len('Hello'))", "print(len('Hello, World'.rjust(20)) - len('Hello, World'))"],
              "Count the padding Python really adds. Running the book's lines shows its printed spaces differ by one."),
         ]),
    dict(id="alternate", name="Alternating case program", title="Program: alternating case", part=5, visual="alternate", layout="below",
         concepts=["Practice Questions"],
         groups=[
             (["flip = lambda i, c: c.lower() if i % 2 == 0 else c.upper()"],
              "A tiny rule: even positions go to lower case, odd positions to upper case."),
             (["print(''.join(flip(i, c) for i, c in enumerate('Hello, world!')))"],
              "enumerate hands out each character with its position. join glues the new characters into one string."),
         ]),
    dict(id="piglatin", name="Pig Latin", title="Program: Pig Latin", part=5, visual="piglatin", layout="below",
         concepts=["A Short Program: Pig Latin"],
         groups=[
             (["cut = lambda w: next((i for i, c in enumerate(w) if c in 'aeiouy'), len(w))"],
              "cut finds where the first vowel sits. That is the length of the opening consonants."),
             (["pig = lambda w: w[cut(w):] + w[:cut(w)] + ('yay' if cut(w) == 0 else 'ay')"],
              "Move the opening consonants to the end and add ay. A word that starts with a vowel just gets yay."),
             (["print(' '.join(pig(w) for w in 'my name is al'.split()))"],
              "split makes the words, pig translates each one, join puts the sentence back together."),
         ]),
    dict(id="tableprinter", name="Table printer", title="Practice program: table printer", part=5, visual="tableprinter", layout="below",
         concepts=["Practice Program: Table Printer"],
         groups=[
             (["a = ['apples', 'oranges', 'cherries', 'banana']", "b = ['Alice', 'Bob', 'Carol', 'David']", "c = ['dogs', 'cats', 'moose', 'goose']", "table = [a, b, c]"],
              "A table is a list of columns. Each column is a list of strings."),
             (["w = [max(len(s) for s in col) for col in table]", "print('\\n'.join(' '.join(s.rjust(w[j]) for j, s in enumerate(r)) for r in zip(*table)))"],
              "A column is as wide as its longest string. zip(*table) turns columns into rows, rjust pads every cell, and join builds each line."),
         ]),
    dict(id="clipboard", name="Clipboard program, without the clipboard", title="Clipboard programs: copy, change, paste", part=5, visual="clipboard", layout="below",
         concepts=["Copying and Pasting Strings", "ClipboardPrograms", "pyperclip.copy", "pyperclip.paste", "Project 2: Add Bullets to Wiki Markup"],
         groups=[
             (["shelf = ['Alice\\nBob\\nCarol']", "text = shelf[0]"],
              "A list of one item stands in for the clipboard here. pyperclip.paste() would hand you that text."),
             (["lines = text.split('\\n')", "shelf[0] = '\\n'.join('* ' + line for line in lines)", "print(shelf[0])"],
              "Split into lines, put a star in front of each, join, and put the result back. pyperclip.copy() would do that last step."),
         ]),
]

# part numbers: 1 literals and reading, 2 formatting, 3 methods, 4 characters and bytes, 5 programs and the clipboard
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
