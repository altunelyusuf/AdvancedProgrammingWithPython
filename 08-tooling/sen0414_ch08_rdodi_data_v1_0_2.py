"""Chapter 8 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter ("Strings and Text Editing") was read on automatetheboringstuff.com on 2026-10-01. The build shell could not use the WebFetch
tool (its permission request was not answered), so the chapter page was downloaded with curl through the session's agent proxy (HTTP 200,
77,792 bytes, page title 'Chapter 8 - Strings and Text Editing, Automate the Boring Stuff with Python, 3rd Ed') and converted to text; its 27
section headings, 33 interactive-shell blocks, its programs and 10 practice questions with 1 practice program were then run or read.
The 31 shell blocks that do not use pyperclip were run as a doctest under Python 3.14.4: 28 gave exactly the printed output, 2 differ only in how the
page shows them (a blank line inside print output, a list wrapped over three lines), and 1 has two wrong printed outputs (rjust(20), see finding F3).
The Python documentation was read from the CPython source tree at tag v3.14.4 (Doc/ files fetched from raw.githubusercontent.com; the commit
hash of the tag could not be obtained because the GitHub API was not reachable from this session), the PEPs from peps.python.org on 2026-10-01, and
the pages at docs.python.org were opened the same day, where they were headed Python 3.14.8. Every behaviour was executed under Python 3.14.4.
pyperclip is not installed on the build machine and there is no clipboard here, so the clipboard itself was NOT executed: the chapter's two clipboard
programs were run unchanged against a stand-in module that keeps the text in a variable, and are labelled so. A claim not in this file was not made."""
__version__ = "1.0.2"
CH = 8
DATE = "2026-10-01"
PYVER = "3.14.4"
TITLE = "Strings and text editing for an advanced course: chapter 8 of the 3rd edition and today's Python"
QUESTION = "What does chapter 8 of the 3rd edition teach about string literals, indexing, formatting, string methods, characters and the clipboard programs, which of its printed outputs and programs still hold under Python 3.14.4, and what must an advanced course add so that it matches current Python?"
CQS = ("Which operations on a string make a new string, which only test it and return a Boolean or a number, and why can none of them change it?",
       "Which printed outputs and concepts of the chapter differ in current Python, and on what source?")
PUBS = [
 ("P01","Automate the Boring Stuff with Python, 3rd edition - Chapter 8, Strings and Text Editing (Al Sweigart, No Starch Press, 2025)","https://automatetheboringstuff.com/3e/chapter8.html",True),
 ("P02","The Python Tutorial, 3. An Informal Introduction to Python - strings, indexing, slicing, immutability (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/introduction.html",False),
 ("P03","The Python Tutorial, 7. Input and Output - fancier output formatting, str and repr (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/inputoutput.html",False),
 ("P04","The Python Standard Library, Built-in Types - string methods, f-strings, t-strings and printf-style formatting (Python 3.14.4 documentation source)","https://docs.python.org/3/library/stdtypes.html",False),
 ("P05","The Python Language Reference, 2. Lexical analysis - string and bytes literals, escape sequences, f-strings and t-strings (Python 3.14.4 documentation source)","https://docs.python.org/3/reference/lexical_analysis.html",False),
 ("P06","The Python Standard Library, string - format specification mini-language, capwords and Template (Python 3.14.4 documentation source)","https://docs.python.org/3/library/string.html",False),
 ("P07","The Python Standard Library, string.templatelib - support for template string literals (Python 3.14.4 documentation source)","https://docs.python.org/3/library/string.templatelib.html",False),
 ("P08","The Python Standard Library, Built-in Functions - ord, chr and open (Python 3.14.4 documentation source)","https://docs.python.org/3/library/functions.html",False),
 ("P09","Unicode HOWTO - code points, encodings, UTF-8 and the default source encoding (Python 3.14.4 documentation source)","https://docs.python.org/3/howto/unicode.html",False),
 ("P10","The Python Standard Library, codecs - error handlers for encoding and decoding (Python 3.14.4 documentation source)","https://docs.python.org/3/library/codecs.html",False),
 ("P11","PEP 498 - Literal String Interpolation (Smith, 2015; Python 3.6)","https://peps.python.org/pep-0498/",False),
 ("P12","PEP 701 - Syntactic formalization of f-strings (Galindo Salgado, Taskaya, Nikolaou and Gomez Macias, 2022; Python 3.12)","https://peps.python.org/pep-0701/",False),
 ("P13","PEP 750 - Template Strings (Baker, van Rossum, Everitt, Aono, Nikolaou and Peck, 2024; Python 3.14)","https://peps.python.org/pep-0750/",False),
 ("P14","PEP 3101 - Advanced String Formatting (Talin, 2006; Python 3.0)","https://peps.python.org/pep-3101/",False),
 ("P15","PEP 686 - Make UTF-8 mode default (Inada, 2022; Python 3.15)","https://peps.python.org/pep-0686/",False),
]
CONCEPTS = [("Section",x) for x in ("Working with Strings","String Literals","Double Quotes","Escape Sequences","Raw Strings","Multiline Strings","Multiline Comments","Indexes and Slices","The in and not in Operators","F-Strings","F-String Alternatives: %s and format()","Useful String Methods","Changing the Case","Checking String Characteristics","Checking the Start or End of a String","Joining and Splitting Strings","Justifying and Centering Text","Removing Whitespace","Numeric Code Points of Characters","Copying and Pasting Strings","Project 2: Add Bullets to Wiki Markup","A Short Program: Pig Latin","Summary","Practice Questions","Practice Program: Table Printer")] + \
 [("Concept",x) for x in ("String literal","Escape sequence","Raw string","Multiline string","Index","Slice","F-string","Unicode code point","Encoding","ClipboardPrograms")] + \
 [("Method",x) for x in ("upper","lower","isupper","islower","isalpha","isalnum","isdecimal","isspace","istitle","startswith","endswith","join","split","rjust","ljust","center","strip","lstrip","rstrip","format","pyperclip.copy","pyperclip.paste")] + \
 [("Function",x) for x in ("ord()","chr()","print()","input()","len()")]
FINDINGS = [
 ("F1","Background","Chapter 8 of the 3rd edition, Strings and Text Editing, teaches string literals in single and double quotes, the five escape sequences of its Table 8-1, raw strings, multiline strings and their use as multiline comments; indexes and slices of strings and the in and not in operators; f-strings and the alternatives %s and format(); the methods upper(), lower(), isupper(), islower(), isalpha(), isalnum(), isdecimal(), isspace(), istitle(), startswith(), endswith(), join(), split(), rjust(), ljust(), center(), strip(), lstrip() and rstrip(); ord() and chr() with a remark on UTF-8; the pyperclip module and the clipboard projects alternatingText.py and bulletPointAdder.py in three steps; the Pig Latin program; and closes with 10 practice questions and the practice program Table Printer.",["P01"]),
 ("F2","Comparative analysis","Nearly everything the chapter prints reproduces under Python 3.14.4: of its 33 interactive-shell blocks, 31 could be run (two use pyperclip) and 28 gave exactly the printed output, two differ only in how the page shows them, and one has two wrong outputs; the programs validateInput.py and feedcat.py print what the chapter shows, pigLat.py prints the chapter's translation of 'My name is AL SWEIGART and I am 4,000 years old.' character for character, bulletPointAdder.py gives the four bulleted lines, and the practice program Table Printer has a solution that prints the chapter's table.",["P01","P02","P04"]),
 ("F3","Comparative analysis","The chapter contains three printing or listing errors that execution exposes: it prints 'Hello'.rjust(20) with 14 leading spaces where Python 3.14.4 gives 15 (the result is 20 characters wide) and 'Hello, World'.rjust(20) with 9 where it gives 8; the walk-through of pigLat.py prints the line suffix_non_letters += word[-1] + suffix_non_letters, which doubles the stored suffix (for 'Wait!!!' it keeps seven exclamation marks instead of three), while the full listing of the program uses suffix_non_letters = word[-1] + suffix_non_letters and is correct; and the output shown for alternatingText.py ends with ThIs: and contains a line break, whereas running the program on the sentence as written ends with tHiS: on one line, so the printed output does not come from the sentence as written, and the cause was not established.",["P01","P04"]),
 ("F4","Comparative analysis","The chapter simplifies three points that the documentation states more widely: its Table 8-1 lists five escape sequences where the language reference lists more, among them \\r, \\a, \\xhh, \\N{name}, \\uxxxx and \\Uxxxxxxxx, and an unrecognised escape keeps its backslash and draws a SyntaxWarning since Python 3.12; the isX() methods are Unicode-aware, so isspace() is True for U+3000, isdecimal() is True for Arabic-Indic digits that int() converts, isdigit() but not isdecimal() is True for a superscript two that int() rejects, and isalnum() is True for an accented letter, which matters for the chapter's password check; and the chapter compares text case-insensitively with lower() while the documentation names casefold() for caseless matching, since upper() turns the German letter sharp s into two letters.",["P01","P04","P05"]),
 ("F5","Comparative analysis","The chapter says the content of an f-string's braces is interpreted as if passed to str(); the documentation says the value is formatted by format() with the text after a colon as format specifier, which for most values equals str() but is different for a class that defines __format__; the same specifier mini-language gives the alignments that rjust(), ljust() and center() give; the chapter's %s and format() alternatives both remain supported, and the documentation warns that printf-style formatting has quirks, such as a tuple being read as the argument list, and names f-strings, str.format() and string.Template as alternatives.",["P01","P04","P06","P03","P14"]),
 ("F6","Contemporary developments","Current Python extends the formatting the chapter presents: the debug specifier = since Python 3.8, the conversions !s, !r and !a, the lifting of f-string restrictions in Python 3.12 so that a field may reuse the f-string's own quote and hold a backslash, and since Python 3.14 the t-string, which has the syntax of an f-string but evaluates to a string.templatelib.Template, not a str, whose strings and interpolations code can process, for example to escape HTML; the t-string is a SyntaxError in Python 3.13.",["P04","P05","P07","P11","P12","P13"]),
 ("F7","Contemporary developments","Current Python has string methods and traps that the chapter leaves out: removeprefix() and removesuffix() since Python 3.9 because strip() removes a set of characters and not a prefix; splitlines(), which splits on all line boundaries where split('\\n') leaves a carriage return on text with Windows line ends and so would leave it in the chapter's bullet adder; split() with no argument against split(' '); partition(); find(), count() and replace(); casefold(); zfill(); and the warning that title() treats an apostrophe as a word boundary, so string.capwords() is offered.",["P04","P06"]),
 ("F8","Contemporary developments","The chapter's advice that 'utf-8' is the correct encoding 99 percent of the time holds, but open() called without an encoding uses the locale encoding in Python 3.14.4, so a file written as UTF-8 cannot be read back in a C locale with UTF-8 mode off, where the decoder reports the ascii codec; PEP 686 makes UTF-8 mode the default only from Python 3.15; the source encoding of a program is UTF-8 by default; chr() accepts only 0 to 0x10FFFF and ord() only a one-character string; and encoding errors can be handled with the errors argument, such as replace, backslashreplace and ignore.",["P01","P08","P09","P10","P15"]),
 ("F9","Conclusion","For an advanced course, chapter 8 is best taught by asking of each string operation whether it makes a new string, tests the string, or is a literal or formatting form, because no operation changes a string in place: the chapter's printed outputs hold under Python 3.14.4 except the two rjust(20) lines and the alternatingText.py output, the pigLat.py walk-through line must be read with the listing, and casefold(), removeprefix(), splitlines(), format specifiers, t-strings, the Unicode behaviour of the isX() methods and the locale encoding of open() are what the chapter leaves for the course to add; the clipboard itself was not executed.",["P01","P02","P04","P05","P08"]),
]
# (top, mid, leaf, exemplar, definition) - the io example is added from IO below
_TAXDEF = [
 ("StringLiterals","StringQuoting","QuoteStyles","'Bob\\'s'","A string literal may begin and end with single or double quotes; the quote that opens it also closes it, so a literal in double quotes can hold a single quote, and inside a single-quoted literal the escape \\' does the same."),
 ("StringLiterals","StringQuoting","EscapeSequences","'Hello there!\\nHow are you?'","An escape sequence is a backslash followed by a character that stands for one character that is hard to type, such as \\n for a newline, \\t for a tab, \\' for a single quote and \\\\ for a backslash; it counts as one character of the string."),
 ("StringLiterals","StringQuoting","StringPrefixes","rb'\\n'","A letter before the opening quote changes how the literal is read: r for raw, f for formatted, b for bytes, u with no effect, and since Python 3.14 t for template strings; r can be combined with f, t and b."),
 ("StringLiterals","StringQuoting","UnrecognizedEscapes","'\\q'","A backslash followed by a character that forms no escape sequence stays in the string as a backslash, and since Python 3.12 the compiler draws a SyntaxWarning; writing the backslash twice or using a raw string avoids it."),
 ("StringLiterals","LiteralForms","RawStrings","r'C:\\Users\\Alice\\Desktop'","A raw string literal, written with an r before the opening quote, treats every backslash as an ordinary character and ignores escape sequences, which suits Windows file paths and regular expressions."),
 ("StringLiterals","LiteralForms","MultilineStrings","'''Dear Alice,\\n\\nBob'''","A multiline string begins and ends with three single or three double quotes and keeps every quote, tab and newline between them as part of the string; the indentation rules of blocks do not apply inside it."),
 ("StringLiterals","LiteralForms","MultilineComments","def say_hello():\\n    '''This function prints hello.'''","A multiline string used as a comment is an ordinary string expression that is evaluated and dropped, except that the string which opens a function body is kept as the function's documentation string."),
 ("StringAccess","Positions","StringIndexing","greeting[-1]","An index in square brackets picks one character, counting from 0 at the front and from -1 at the back; a character is a string of length one, and an index past the end raises IndexError."),
 ("StringAccess","Positions","StringSlicing","greeting[7:-1]","A slice string[start:end] is a new string of the characters from start up to but not including end; omitted ends mean the front or the back, an end past the string is cut short, a step is allowed, and the original string is left as it was."),
 ("StringAccess","StringProperties","StringImmutability","name[7] = 'the'","A string cannot be changed after it is made: assigning to an index raises TypeError, and methods such as upper() return a new string, so a changed text is built from slices or assigned back to the name."),
 ("StringAccess","StringProperties","InOperator","'Hello' in 'Hello, World'","The in and not in operators test whether the first string occurs as a run of characters inside the second, with capitalisation counted, and give True or False; the empty string is in every string."),
 ("StringFormatting","FormatInterpolation","FStrings","f'My name is {name}. I am {age} years old.'","An f-string is a literal with an f before the opening quote in which each expression between curly brackets is evaluated and its value put into the text; doubled brackets stand for one literal bracket."),
 ("StringFormatting","FormatInterpolation","FormatSpecifiers","f'{3.14159:.2f}'","After a colon in a replacement field comes a format specifier passed to format(), which sets fill, alignment with <, > or ^, width, sign, thousands separator and precision, so it does the work of rjust(), ljust() and center() and more."),
 ("StringFormatting","FormatInterpolation","DebugAndConversions","f'{name=}'","An equals sign after the expression prints the expression text, the sign and the value, and the conversions !s, !r and !a apply str(), repr() or ascii() before formatting; since Python 3.12 a field may also reuse the f-string's own quote and hold a backslash."),
 ("StringFormatting","FormatInterpolation","TemplateStrings","t'Hello {name}'","A template string, written with a t prefix since Python 3.14, has the syntax of an f-string but evaluates to a Template object that keeps the literal parts and the interpolations separate, so code can process them, for instance to escape HTML, before making a string."),
 ("StringFormatting","OlderStyles","Concatenation","'Hello, my name is ' + name + '. I am ' + str(age) + ' years old.'","Strings are joined with + and repeated with *, and a number must first be turned into a string with str(); two literals written next to each other are joined at compile time."),
 ("StringFormatting","OlderStyles","PercentFormatting","'My name is %s. I am %s years old.' % (name, age)","The % operator on a string replaces conversion specifiers such as %s, %d and %f with the values of a tuple or a mapping; it still works, but a single tuple operand is read as the list of arguments and the documentation names f-strings and format() as alternatives."),
 ("StringFormatting","OlderStyles","FormatMethod","'{1} years ago, {0} was born and named {0}.'.format(name, age)","The format() method replaces curly-bracket fields with its arguments, by position, by index or by name, and accepts the same format specifiers as an f-string."),
 ("StringMethods","TextCase","ChangingCase","spam = spam.upper()","The upper() and lower() methods return a new string with every letter converted and leave other characters alone; the original is unchanged, so the result is assigned back or compared at once, as in a case-insensitive check."),
 ("StringMethods","TextCase","CaseTests","'HELLO'.isupper()","isupper() and islower() return True when the string has at least one cased letter and all its cased letters are upper or lower case, and False for an empty string or one with no letters."),
 ("StringMethods","TextCase","CaseFolding","'stra\\xdfe'.casefold() == 'strasse'","casefold() is a stronger lower() meant for caseless matching: it turns the German sharp s into ss, so text that differs only by case compares equal, where lower() leaves that letter alone and upper() makes the string longer."),
 ("StringMethods","TextCase","MethodChaining","'Hello'.upper().lower().upper()","A method that returns a string can be followed by another method call on the result, forming a chain; a method that returns a Boolean or a number ends the chain."),
 ("StringMethods","TextChecks","CharacterTests","'hello123'.isalnum()","The methods isalpha(), isalnum(), isdecimal(), isspace() and istitle() return True only for a non-empty string whose characters all fit the kind named, so they validate input and are False for an empty string."),
 ("StringMethods","TextChecks","UnicodeDigits","'\\u0663'.isdecimal()","The isX() methods use the Unicode database, not ASCII: isdecimal() is True for any decimal digit of any script, isdigit() also for a superscript digit, isspace() for U+3000, and isalpha() and isalnum() for accented letters; isascii() tests for ASCII only."),
 ("StringMethods","TextChecks","StartsEndsWith","'Hello, world!'.startswith('Hello') and 'abc'.endswith('c')","startswith() and endswith() test only the beginning or the end of a string and also accept a tuple of alternatives, which is shorter than slicing and comparing."),
 ("StringMethods","JoiningAndSplittingText","JoinMethod","'-'.join(c for c in 'abc')","join() is called on the separator string and given an iterable of strings; it returns them concatenated with the separator between, and raises TypeError for an item that is not a string."),
 ("StringMethods","JoiningAndSplittingText","SplitMethod","'My name is Simon'.split('m')","split(sep) cuts a string at each occurrence of the separator and returns a list; consecutive separators give empty strings, and splitting the empty string gives a list holding one empty string."),
 ("StringMethods","JoiningAndSplittingText","WhitespaceSplit","'My name is Simon'.split()","split() with no argument cuts at runs of whitespace, ignores whitespace at the ends and gives an empty list for an empty or blank string, unlike split(' ')."),
 ("StringMethods","JoiningAndSplittingText","SplitLines","text.splitlines()","splitlines() cuts a string at every line boundary, including the carriage-return line feed of Windows text, and drops the final empty item that split('\\n') leaves after a trailing newline."),
 ("StringMethods","JoiningAndSplittingText","PartitionMethod","'Monty Python'.partition(' ')","partition(sep) cuts at the first occurrence and returns a tuple of the part before, the separator and the part after, or the string and two empty strings when the separator is absent; rpartition() cuts at the last."),
 ("StringMethods","TextSpacing","JustifyMethods","'Hello'.rjust(20, '*')","rjust(), ljust() and center() return a string padded to a given width with spaces or one fill character; a width no larger than the string changes nothing, and the padding is 15 spaces for 'Hello'.rjust(20)."),
 ("StringMethods","TextSpacing","StripMethods","'SpamSpamBaconSpamEggsSpamSpam'.strip('ampS')","strip(), lstrip() and rstrip() remove whitespace from both ends, the left or the right, or, with an argument, any of the characters in that argument in any order, which is a set and not a prefix."),
 ("StringMethods","TextSpacing","PrefixSuffixRemoval","'Arthur: three!'.removeprefix('Arthur: ')","removeprefix() and removesuffix(), added in Python 3.9, remove one exact prefix or suffix if present and otherwise return the string unchanged, which is what a programmer who reaches for lstrip() with a word usually wants."),
 ("StringMethods","Searching","FindAndCount","'spam eggs spam'.find('spam', 1) != -1","find() returns the index of the first occurrence at or after an optional start, or -1 when there is none, where index() raises ValueError; count() returns the number of non-overlapping occurrences."),
 ("StringMethods","Searching","ReplaceMethod","'spam, spam'.replace('spam', 'eggs', 1)","replace(old, new) returns a new string with every occurrence of old replaced by new, or only the first count of them when count is given; an empty new deletes old."),
 ("CharactersAndBytes","CodePointConversion","OrdAndChr","ord('A')","Every character has a Unicode code point, an integer from 0 to 0x10FFFF; ord() gives the code point of a one-character string and chr() gives the character of a code point, so ord('A') is 65 and chr(ord('A') + 1) is 'B'."),
 ("CharactersAndBytes","TextEncodings","Utf8Encoding","len('caf\\xe9'.encode('utf-8')) == 5","Encoding turns text into bytes and decoding turns bytes back into text; in UTF-8 a character takes one to four bytes, so a string of four characters can be five bytes long, and encode() and decode() must use the same encoding."),
 ("CharactersAndBytes","TextEncodings","EncodeDecodeErrors","'caf\\xe9'.encode('ascii', errors='replace')","A character the encoding cannot represent raises UnicodeEncodeError and bytes that do not form valid text raise UnicodeDecodeError, unless the errors argument names another handler such as replace, backslashreplace or ignore; decoding with the wrong encoding can succeed and give wrong text."),
 ("CharactersAndBytes","TextEncodings","FileEncoding","open('note.txt', 'w', encoding='utf-8')","A text file is turned into bytes by an encoding; open() called without one uses the locale encoding in Python 3.14, which is why a program should name encoding='utf-8' when it writes or reads text it means to share."),
 ("ClipboardAndPrograms","ClipboardPrograms","ClipboardModule","pyperclip.paste()","The third-party pyperclip module copies text to and from the computer's clipboard with copy() and paste(); it is not part of Python, so a program that imports it fails with ModuleNotFoundError where it is not installed."),
 ("ClipboardAndPrograms","ProjectPrograms","BulletPointAdder","lines[i] = '* ' + lines[i]","The bullet program takes text from the clipboard, splits it into lines, puts a star and a space before each and joins the lines back, so the four lines of the chapter's list come back as four bulleted lines."),
 ("ClipboardAndPrograms","ProjectPrograms","AlternatingText","make_uppercase = not make_uppercase","The alternating-text program walks over the characters of a string and switches between lower and upper case on every character, spaces and punctuation included, so the pattern of a word depends on its position in the text."),
 ("ClipboardAndPrograms","ProjectPrograms","InputValidation","if age.isdecimal(): break","The validation program repeats a question with a while loop until isdecimal() accepts the age and isalnum() accepts the password, and rejects 'forty two' and 'secr3t!'."),
 ("ClipboardAndPrograms","ProjectPrograms","PigLatin","prefix_consonants += word[0]","The Pig Latin program splits a message into words, sets aside punctuation at both ends, moves leading consonants to the end followed by ay, adds yay to words that start with a vowel or y, and restores upper or title case."),
 ("ClipboardAndPrograms","ProjectPrograms","TablePrinter","printTable(tableData)","The practice program prints a list of lists of strings as a table with right-justified columns, each as wide as its longest string, found first with a loop over the lists."),
]
_IO = {}
_IO['QuoteStyles'] = ("(__import__('ast').literal_eval('\\x22Alice\\'s cat\\x22') == 'Alice\\'s cat', len('Bob\\'s'), '\\x22' == chr(34))", '(True, 5, True)')
_IO['EscapeSequences'] = ("('a\\tb', 'a\\\\b', 'line1\\nline2'.split('\\n'), len('\\\\'), len('\\n'))", "('a\\tb', 'a\\\\b', ['line1', 'line2'], 1, 1)")
_IO['UnrecognizedEscapes'] = ("(lambda cw: (cw.__enter__(), __import__('warnings').simplefilter('ignore'), list(__import__('ast').literal_eval('\\'\\\\q\\'')), cw.__exit__(None, None, None))[2])(__import__('warnings').catch_warnings())", "['\\\\', 'q']")
_IO['StringPrefixes'] = ("(type(b'a').__name__, type(r'a').__name__, type(u'a').__name__, b'A'[0], len(rb'\\n'))", "('bytes', 'str', 'str', 65, 2)")
_IO['RawStrings'] = ("(len(r'\\n'), len('\\n'), r'C:\\Users\\Al' == 'C:\\\\Users\\\\Al')", '(2, 1, True)')
_IO['MultilineStrings'] = ("__import__('ast').literal_eval('\\'\\'\\'Dear Al,\\n\\nBob\\'\\'\\'').split('\\n')", "['Dear Al,', '', 'Bob']")
_IO['MultilineComments'] = ("(lambda ns: (exec('def f():\\n    \\'\\'\\'Says hi.\\'\\'\\'\\n', ns), ns['f'].__doc__)[1])({})", "'Says hi.'")
_IO['StringIndexing'] = ("('Hello, world!'[0], 'Hello, world!'[4], 'Hello, world!'[-1], len('Hello, world!'))", "('H', 'o', '!', 13)")
_IO['StringSlicing'] = ("('Hello, world!'[0:5], 'Hello, world!'[:5], 'Hello, world!'[7:-1], 'Hello, world!'[7:], 'Hello, world!'[::-1])", "('Hello', 'Hello', 'world', 'world!', '!dlrow ,olleH')")
_IO['StringImmutability'] = ("(lambda s: (s.upper(), s))('abc')", "('ABC', 'abc')")
_IO['InOperator'] = ("('Hello' in 'Hello, World', 'HELLO' in 'Hello, World', '' in 'spam', 'cats' not in 'cats and dogs')", '(True, False, True, False)')
_IO['FStrings'] = ("(lambda name, age: f'My name is {name}. I am {age} years old. In ten years I will be {age + 10}. {{name}}')('Al', 4000)", "'My name is Al. I am 4000 years old. In ten years I will be 4010. {name}'")
_IO['FormatSpecifiers'] = ("f'{3.14159:.2f}|{42:>6}|{42:^6}|{42:06}|{1234567:,}|{255:#x}|{0.256:.1%}'", "'3.14|    42|  42  |000042|1,234,567|0xff|25.6%'")
_IO['DebugAndConversions'] = ("(lambda s, n: (f'{s=}', f'{n + 1 = }', f'{s!r} {s!s}', f'{chr(233)!a}'))('Al', 41)", '("s=\'Al\'", \'n + 1 = 42\', "\'Al\' Al", "\'\\\\xe9\'")')
_IO['Concatenation'] = ("(lambda name, age: ('Hello, my name is ' + name + '. I am ' + str(age) + ' years old.', 'Py' 'thon', 3 * 'un' + 'ium'))('Al', 4000)", "('Hello, my name is Al. I am 4000 years old.', 'Python', 'unununium')")
_IO['PercentFormatting'] = ("('My name is %s. I am %s years old.' % ('Al', 4000), '%05.1f|%-4s|%3d%%' % (3.14159, 'ab', 7))", "('My name is Al. I am 4000 years old.', '003.1|ab  |  7%')")
_IO['FormatMethod'] = ("('{1} years ago, {0} was born and named {0}.'.format('Al', 4000), '{name} is {age}'.format(name='Al', age=4000))", "('4000 years ago, Al was born and named Al.', 'Al is 4000')")
_IO['ChangingCase'] = ("('Hello, world!'.upper(), 'Hello, world!'.lower(), 'great' == 'GREat'.lower())", "('HELLO, WORLD!', 'hello, world!', True)")
_IO['CaseTests'] = ("('Hello, world!'.isupper(), 'HELLO'.isupper(), 'abc12345'.islower(), '12345'.islower(), ''.islower())", '(False, True, True, False, False)')
_IO['CaseFolding'] = ("('stra\\xdfe'.lower() == 'strasse', 'stra\\xdfe'.casefold() == 'strasse', len('stra\\xdfe'.upper()))", '(False, True, 7)')
_IO['MethodChaining'] = ("('Hello'.upper().lower().upper(), 'HELLO'.lower().islower(), 'a-b'.upper().replace('-', '+'))", "('HELLO', True, 'A+B')")
_IO['CharacterTests'] = ("('hello'.isalpha(), 'hello123'.isalpha(), 'hello123'.isalnum(), '123'.isdecimal(), '    '.isspace(), 'This Is Title Case'.istitle(), ''.isalpha())", '(True, False, True, True, True, True, False)')
_IO['UnicodeDigits'] = ("('\\xb2'.isdecimal(), '\\xb2'.isdigit(), '\\u0663'.isdecimal(), int('\\u0663'), '\\u3000'.isspace(), '\\xe9'.isalpha() and not '\\xe9'.isascii())", '(False, True, True, 3, True, True)')
_IO['StartsEndsWith'] = ("('Hello, world!'.startswith('Hello'), 'abc123'.endswith('12'), 'notes.txt'.endswith(('.py', '.txt')))", '(True, False, True)')
_IO['JoinMethod'] = ("(', '.join(['cats', 'rats', 'bats']), 'ABC'.join(['My', 'name']), '-'.join('abc'))", "('cats, rats, bats', 'MyABCname', 'a-b-c')")
_IO['SplitMethod'] = ("('MyABCnameABCisABCSimon'.split('ABC'), 'My name is Simon'.split('m'), '1,,2'.split(','), ''.split(','))", "(['My', 'name', 'is', 'Simon'], ['My na', 'e is Si', 'on'], ['1', '', '2'], [''])")
_IO['WhitespaceSplit'] = ("('My name is Simon'.split(), '  a \\t b\\n c  '.split(), ''.split(), '  a  b '.split(' '))", "(['My', 'name', 'is', 'Simon'], ['a', 'b', 'c'], [], ['', '', 'a', '', 'b', ''])")
_IO['SplitLines'] = ("('one\\r\\ntwo\\nthree'.split('\\n'), 'one\\r\\ntwo\\nthree'.splitlines(), 'a\\n\\nb\\n'.split('\\n'), 'a\\n\\nb\\n'.splitlines())", "(['one\\r', 'two', 'three'], ['one', 'two', 'three'], ['a', '', 'b', ''], ['a', '', 'b'])")
_IO['PartitionMethod'] = ("('Monty Python'.partition(' '), 'Monty Python'.partition('-'), 'a.b.c'.rpartition('.'))", "(('Monty', ' ', 'Python'), ('Monty Python', '', ''), ('a.b', '.', 'c'))")
_IO['JustifyMethods'] = ("('Hello'.rjust(10), 'Hello'.ljust(10, '-'), 'Hello'.center(20, '='), 'Hello'.rjust(20) == ' ' * 15 + 'Hello', 'Hello'.center(4))", "('     Hello', 'Hello-----', '=======Hello========', True, 'Hello')")
_IO['StripMethods'] = ("('    Hello, World    '.strip(), '    Hello, World    '.lstrip(), 'SpamSpamBaconSpamEggsSpamSpam'.strip('ampS'), 'SpamSpamBaconSpamEggsSpamSpam'.strip('Spam') == 'SpamSpamBaconSpamEggsSpamSpam'.strip('mapS'))", "('Hello, World', 'Hello, World    ', 'BaconSpamEggs', True)")
_IO['PrefixSuffixRemoval'] = ("('Arthur: three!'.lstrip('Arthur: '), 'Arthur: three!'.removeprefix('Arthur: '), 'report.txt'.removesuffix('.txt'), 'report.txt'.removesuffix('.py'))", "('ee!', 'three!', 'report', 'report.txt')")
_IO['FindAndCount'] = ("('spam eggs spam'.find('spam'), 'spam eggs spam'.find('spam', 1), 'spam'.find('x'), 'spam eggs spam'.count('spam'), 'aaaa'.count('aa'))", '(0, 10, -1, 2, 2)')
_IO['ReplaceMethod'] = ("('spam, spam, spam'.replace('spam', 'eggs'), 'spam, spam, spam'.replace('spam', 'eggs', 1), 'abc'.replace('b', ''))", "('eggs, eggs, eggs', 'eggs, spam, spam', 'ac')")
_IO['OrdAndChr'] = ("(ord('A'), ord('4'), ord('!'), chr(65), chr(ord('A') + 1), ord('A') < ord('B'), ord('\\u20ac'), chr(8364) == '\\u20ac', ord('\\U0001f40d'))", "(65, 52, 33, 'A', 'B', True, 8364, True, 128013)")
_IO['Utf8Encoding'] = ("('caf\\xe9'.encode('utf-8'), len('caf\\xe9'), len('caf\\xe9'.encode('utf-8')), 'caf\\xe9'.encode('utf-8').decode('utf-8') == 'caf\\xe9')", "(b'caf\\xc3\\xa9', 4, 5, True)")
_IO['EncodeDecodeErrors'] = ("(ascii(b'caf\\xc3\\xa9'.decode('latin-1')), 'caf\\xe9'.encode('ascii', errors='replace'))", '("\'caf\\\\xc3\\\\xa9\'", b\'caf?\')')
_IO['FileEncoding'] = ("(lambda io, b: (lambda w: (w.write('caf\\xe9'), w.flush(), b.getvalue())[2])(io.TextIOWrapper(b, encoding='utf-8')))(__import__('io'), __import__('io').BytesIO())", "b'caf\\xc3\\xa9'")
_IO['BulletPointAdder'] = ("'\\n'.join('* ' + line for line in 'Lists of animals\\nLists of cultivars'.split('\\n'))", "'* Lists of animals\\n* Lists of cultivars'")
_IO['AlternatingText'] = ("(lambda text: ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text)))('Hello, world!')", "'hElLo, WoRlD!'")
_IO['InputValidation'] = ("('42'.isdecimal(), 'forty two'.isdecimal(), 'secr3t'.isalnum(), 'secr3t!'.isalnum())", '(True, False, True, False)')
_IO['PigLatin'] = ("[(lambda w: (lambda i: w[i:] + (w[:i] + 'ay' if i else 'yay'))(next((k for k, c in enumerate(w) if c in 'aeiouy'), len(w))))(w) for w in ('sweigart', 'old', 'chair', 'years')]", "['eigartsway', 'oldyay', 'airchay', 'yearsyay']")
_IO['TablePrinter'] = ("(lambda t: [''.join(' ' + col[r].rjust(max(map(len, col))) for col in t) for r in range(len(t[0]))])([['apples', 'oranges', 'cherries', 'banana'], ['Alice', 'Bob', 'Carol', 'David'], ['dogs', 'cats', 'moose', 'goose']])", "['   apples Alice  dogs', '  oranges   Bob  cats', ' cherries Carol moose', '   banana David goose']")
TAX = [(t, m, l, e, d, _IO.get(l)) for t, m, l, e, d in _TAXDEF]
ERRORS = []
CLAIMS = [
 ("type('Hello'[0]).__name__", "'str'"),
 ("(lambda s: all(s[:i] + s[i:] == s for i in range(-3, 20)))('Hello, world!')", "True"),
 ("('gg' in 'eggs', 'gg' in ['eggs'])", "(True, False)"),
 ("'123'.upper().isupper()", "False"),
 ("'spam'.count('')", "5"),
 ("'spam, spam'.replace('spam', 'eggs', count=1)", "'eggs, spam'"),
 ("eval(\"'''\\\\\\nab\\ncd'''\")", "'ab\\ncd'"),
 ("(ord(chr(0x10ffff)), 'Hello'.rjust(3) == 'Hello', ' \\t\\n'.isspace())", "(1114111, True, True)"),
 ("'12345'.isupper()", "False"),
 ("\"It's\".istitle()", "False"),
 ("'My name is AL SWEIGART and I am 4,000 years old.'.split()", "['My', 'name', 'is', 'AL', 'SWEIGART', 'and', 'I', 'am', '4,000', 'years', 'old.']"),
 ("'4,000'.isalpha()", "False"),
 ("'Hello'.center(20).count(' ')", "15"),
 ("[hasattr(str, m) for m in ('removeprefix', 'removesuffix', 'casefold', 'splitlines', 'partition', 'zfill')]", "[True, True, True, True, True, True]"),
]
S = "(Sweigart, 2025)"; PSF = "(Python Software Foundation, 2026)"; SM = "(Smith, 2015)"; GS = "(Galindo Salgado et al., 2022)"; BK = "(Baker et al., 2024)"; TL = "(Talin, 2006)"; IN = "(Inada, 2022)"
BODY = {
 "StringLiterals": "How a program writes text in its source, with quotes, escape sequences and prefixes, opens Chapter 8 " + S + ".",
 "StringQuoting": "The chapter shows how to put a quotation mark or another hard-to-type character inside a string literal " + S + ".",
 "QuoteStyles": "A literal may begin and end with single or double quotes, so the chapter's literal about Alice's cat is written with double quotes and needs no escape, and 'Bob\\'s' with an escape has length 5 " + S + "; the question about Howl's Moving Castle has the same answer, that the double quotes make the single quote ordinary; the reference adds that the choice of quote does not otherwise change how a literal is read " + PSF + ".",
 "EscapeSequences": "Table 8-1 lists five escape sequences, the escapes for a single quote, a double quote, a tab, a newline and a backslash, and 'a\\tb' has three characters because the tab is one; 'line1\\nline2'.split('\\n') is ['line1', 'line2'] and '\\\\' has length 1 " + S + "; the language reference lists more, among them \\a \\b \\f \\r \\v, \\ooo, \\xhh, \\N{name}, \\uxxxx and \\Uxxxxxxxx and a backslash at a line end that joins two lines, and '\\x41' and '\\101' are both 'A', '\\N{SNAKE}' is one character, which the chapter as read does not present " + PSF + ".",
 "UnrecognizedEscapes": "In '\\q' the backslash is kept, so list('\\\\q') is ['\\\\', 'q'], and compiling it draws a SyntaxWarning, which Python 3.12 introduced after a DeprecationWarning that began with Python 3.6, and a later version is to make it a SyntaxError; the chapter as read does not present it, and its advice to use raw strings for regular expressions avoids it " + S + " " + PSF + ".",
 "StringPrefixes": "The chapter uses the r prefix and the f prefix; the reference lists b, r, f, t and u, where u has no effect, and lets r combine with f, t and b, so type(b'a') is bytes while type(r'a') and type(u'a') are str and len(rb'\\n') is 2 " + S + " " + PSF + ".",
 "LiteralForms": "A literal can be raw, spread over several lines or used as a comment " + S + ".",
 "RawStrings": "print(r'The file is in C:\\Users\\Alice\\Desktop') prints the path as written, r'Hello...\\n\\n...world!' prints the backslash pairs where the ordinary literal prints two line breaks, and len(r'\\n') is 2 while len('\\n') is 1 " + S + "; the chapter names Windows paths and regular expressions as the uses " + S + ".",
 "MultilineStrings": "Triple quotes keep the quotes, tabs and newlines between them: the feedcat.py letter to Alice as a triple-quoted string is equal to the one-line form with \\n, holds five newlines, and needs no escape for the single quote in Eve's " + S + "; the indentation rules of blocks do not apply inside it, and eval of a triple-quoted Dear Al, blank line Bob gives the split ['Dear Al,', '', 'Bob']; a backslash right after the opening quotes drops the first newline " + PSF + ".",
 "MultilineComments": "The chapter uses a multiline string as a comment before a function and as the text under def say_hello() " + S + "; Python does not treat it as a comment but as a string, and the one that opens a function body is kept: executing a def whose body starts with a triple-quoted 'Says hi.' gives that text as the function's __doc__, which the chapter as read does not name " + PSF + ".",
 "StringAccess": "Strings are read like lists and tested with in " + S + ".",
 "Positions": "An index picks one character and a slice a run of characters " + S + ".",
 "StringIndexing": "'Hello, world!' has 13 characters, index 0 is 'H', index 4 is 'o' and -1 is '!', a space before the bracket as in greeting [4] is allowed, and greeting[13] raises IndexError: string index out of range " + S + "; there is no separate character type, since 'Hello'[0] is itself a str " + PSF + ".",
 "StringSlicing": "greeting[0:5] and greeting[:5] are 'Hello', greeting[7:-1] is 'world', greeting[7:] is 'world!' and the original stays 'Hello, world!' " + S + "; a slice past the end is cut short, so greeting[7:99] is 'world!' and greeting[99:] is '', a step is allowed so greeting[::-1] is '!dlrow ,olleH', and s[:i] + s[i:] equals s for every i " + PSF + ".",
 "StringProperties": "A string is immutable, and in tests for a substring " + S + ".",
 "StringImmutability": "name[7] = 'the' on 'Zophie a cat' raises TypeError: 'str' object does not support item assignment, and the changed text is built as name[0:7] + 'the' + name[8:12], 'Zophie the cat' " + S + "; 'age ' + 4000 raises TypeError and 'age ' + str(4000) is 'age 4000', and the chapter's point that spam.upper() leaves spam alone is the same immutability " + S + " " + PSF + ".",
 "InOperator": "'Hello' in 'Hello, World' is True, 'HELLO' in 'Hello, World' is False because capitals count, '' in 'spam' is True and 'cats' not in 'cats and dogs' is False " + S + "; on a list the operator tests whole items, so 'gg' in 'eggs' is True while 'gg' in ['eggs'] is False " + PSF + ".",
 "StringFormatting": "Putting one string inside another is done with f-strings and their predecessors " + S + ".",
 "FormatInterpolation": "The chapter presents the f-string, and current Python adds specifiers, debug output and template strings " + S + " " + PSF + ".",
 "FStrings": "f'My name is {name}. I am {age} years old. In ten years I will be {age + 10}. {{name}}' with name 'Al' and age 4000 gives 'My name is Al. I am 4000 years old. In ten years I will be 4010. {name}' " + S + "; the chapter says the content of the brackets is interpreted as if passed to str(), and the documentation says the value is formatted by format(), which for most values gives the same text " + PSF + "; f-strings came in Python 3.6 " + SM + ".",
 "FormatSpecifiers": "f'{3.14159:.2f}|{42:>6}|{42:^6}|{42:06}|{1234567:,}|{255:#x}|{0.256:.1%}' gives '3.14|    42|  42  |000042|1,234,567|0xff|25.6%', and f'{s:>10}', f'{s:<10}', f'{s:^20}' and f'{s:*^20}' equal s.rjust(10), s.ljust(10), s.center(20) and s.center(20, '*'); a class with its own __format__ receives the text after the colon, so f'{c:.1f}' can differ from str(c), which is why the chapter's statement about str() holds only by default; the chapter as read does not present specifiers " + S + " " + PSF + " " + TL + ".",
 "DebugAndConversions": "f'{s=}' with s = 'Al' gives the text s='Al', f'{n + 1 = }' keeps its spaces and gives 'n + 1 = 42', f'{s!r} {s!s}' gives the text 'Al' Al and f'{chr(233)!a}' gives the escaped form of the accented e; since Python 3.12 an f-string written in double quotes may hold a double-quoted dictionary key in a field, and a backslash inside a field is allowed, and the chapter as read does not present these " + S + " " + PSF + " " + GS + ".",
 "TemplateStrings": "t'Hello {name}, you are {age:>6} years old.' has type Template, isinstance(t, str) is False, t.strings is ('Hello ', ', you are ', ' years old.') and its interpolations hold the expression, value, conversion and specifier, for example ('age', 4000, None, '>6'); a function that escapes the interpolated value of t'<p>{evil}</p>' gives <p>&lt;b&gt;x&lt;/b&gt;</p> where the f-string gives the raw tag; Python 3.13 rejects the t prefix with a SyntaxError, so these examples were run under Python 3.14.4 only and not in the page, and the chapter as read does not present them " + PSF + " " + BK + ".",
 "OlderStyles": "Concatenation, the % operator and format() are the ways before the f-string " + S + ".",
 "Concatenation": "'Hello, my name is ' + name + '. I am ' + str(age) + ' years old.' gives 'Hello, my name is Al. I am 4000 years old.' and needs str(age) " + S + "; two literals side by side are joined, 'Py' 'thon' being 'Python', and 3 * 'un' + 'ium' is 'unununium' " + PSF + ".",
 "PercentFormatting": "'My name is %s. I am %s years old.' % (name, age) gives 'My name is Al. I am 4000 years old.' and '%05.1f|%-4s|%3d%%' % (3.14159, 'ab', 7) gives '003.1|ab  |  7%' " + S + "; '%s' % (1, 2) raises TypeError because the tuple is read as two arguments for one specifier, '%s' % ((1, 2),) is '(1, 2)', and the documentation notes the quirks of this style and names f-strings, str.format() and string.Template " + PSF + ".",
 "FormatMethod": "'{1} years ago, {0} was born and named {0}.'.format(name, age) gives '4000 years ago, Al was born and named Al.' and '{name} is {age}'.format(name='Al', age=4000) gives 'Al is 4000' " + S + "; too few arguments raise IndexError: Replacement index 1 out of range for positional args tuple, and format() was specified for Python 3.0 " + TL + " " + PSF + ".",
 "StringMethods": "A string method returns a new value and never changes the string it is called on " + S + ".",
 "TextCase": "Methods that convert or test the case of letters " + S + ".",
 "ChangingCase": "'Hello, world!'.upper() is 'HELLO, WORLD!' and .lower() is 'hello, world!', the string spam stays unchanged until spam = spam.upper() assigns the result, and 'great' == 'GREat'.lower() is True, which is the chapter's case-insensitive answer to the question How are you? " + S + ".",
 "CaseTests": "'Hello, world!'.isupper() and islower() are both False, 'HELLO'.isupper() and 'abc12345'.islower() are True, '12345'.islower() and '12345'.isupper() are False, and ''.islower() is False because at least one cased letter is needed " + S + " " + PSF + "; 'Hello'.upper().isupper() is True but '123'.upper().isupper() is False for the same reason " + PSF + ".",
 "CaseFolding": "'stra\\xdfe'.lower() == 'strasse' is False and 'stra\\xdfe'.casefold() == 'strasse' is True, and len('stra\\xdfe') is 6 while len('stra\\xdfe'.upper()) is 7 because upper() gives STRASSE; the chapter compares with lower() and as read does not name casefold() " + S + " " + PSF + ".",
 "MethodChaining": "'Hello'.upper().lower().upper() is 'HELLO', 'HELLO'.lower().islower() is True and 'a-b'.upper().replace('-', '+') is 'A+B' " + S + "; islower() returns a Boolean, so nothing can be chained after it " + PSF + ".",
 "TextChecks": "Methods that test what kind of characters a string holds or how it begins and ends " + S + ".",
 "CharacterTests": "'hello'.isalpha() is True, 'hello123'.isalpha() is False, 'hello123'.isalnum() is True, '123'.isdecimal() is True, '    '.isspace() is True and 'This Is Title Case'.istitle() is True " + S + "; every one of them is False for the empty string, and '4,000'.isalpha() is False " + PSF + ".",
 "UnicodeDigits": "'\\xb2'.isdecimal() is False while '\\xb2'.isdigit() is True, '\\u0663'.isdecimal() is True and int('\\u0663') is 3, '\\u3000'.isspace() is True and an accented e is alphabetic but not ASCII, so 'caf\\xe9'.isalnum() is True and 'caf\\xe9'.isascii() is False; the chapter describes isspace() as spaces, tabs and newlines and as read does not mention the Unicode behaviour, so its password check with isalnum() accepts accented letters " + S + " " + PSF + ".",
 "StartsEndsWith": "'Hello, world!'.startswith('Hello') and .endswith('world!') are True, 'abc123'.startswith('abcdef') and .endswith('12') are False " + S + "; both accept a tuple, so 'notes.txt'.endswith(('.py', '.txt')) is True " + PSF + ".",
 "JoiningAndSplittingText": "join() and split() convert between a list of strings and one string " + S + ".",
 "JoinMethod": "', '.join(['cats', 'rats', 'bats']) is 'cats, rats, bats' and 'ABC'.join(['My', 'name']) is 'MyABCname' " + S + "; join accepts any iterable of strings, so '-'.join('abc') is 'a-b-c', and ', '.join([1, 2]) raises TypeError: sequence item 0: expected str instance, int found " + PSF + ".",
 "SplitMethod": "'MyABCnameABCisABCSimon'.split('ABC') is ['My', 'name', 'is', 'Simon'] and 'My name is Simon'.split('m') is ['My na', 'e is Si', 'on'], and splitting the chapter's multiline letter on '\\n' gives seven items with an empty string for the blank line " + S + "; '1,,2'.split(',') keeps the empty item and ''.split(',') is [''] " + PSF + ".",
 "WhitespaceSplit": "'My name is Simon'.split() is ['My', 'name', 'is', 'Simon'] " + S + "; with no argument runs of whitespace are one separator, so '  a \\t b\\n c  '.split() is ['a', 'b', 'c'] and ''.split() is [], while '  a  b '.split(' ') is ['', '', 'a', '', 'b', ''] " + PSF + ".",
 "SplitLines": "The chapter splits the clipboard text with split('\\n') " + S + "; on 'one\\r\\ntwo\\nthree' that gives ['one\\r', 'two', 'three'] and splitlines() gives ['one', 'two', 'three'], and on 'a\\n\\nb\\n' split gives a trailing empty string and splitlines does not; splitlines() also cuts at \\x0b, \\x1c and \\u2028, and the chapter as read does not present it " + PSF + ".",
 "PartitionMethod": "'Monty Python'.partition(' ') is ('Monty', ' ', 'Python'), 'Monty Python'.partition('-') is ('Monty Python', '', '') and 'a.b.c'.rpartition('.') is ('a.b', '.', 'c'); the chapter as read does not present it " + S + " " + PSF + ".",
 "TextSpacing": "Padding and trimming change the width of a string by its ends " + S + ".",
 "JustifyMethods": "'Hello'.rjust(10) is five spaces and Hello, 'Hello'.ljust(10, '-') is 'Hello-----' and 'Hello'.center(20, '=') is '=======Hello========', with the extra padding on the right here, 7 left and 8 right " + S + "; 'Hello'.rjust(20) has 15 spaces, which the chapter prints as 14, and 'Hello, World'.rjust(20) has 8, which it prints as 9, so both printed lines disagree with Python 3.14.4; a fill of two characters raises TypeError, a width no larger than the string changes nothing, and the f-string specifiers > < ^ give the same results " + S + " " + PSF + ".",
 "StripMethods": "'    Hello, World    '.strip() is 'Hello, World', lstrip() keeps the right spaces, and 'SpamSpamBaconSpamEggsSpamSpam'.strip('ampS') is 'BaconSpamEggs' " + S + "; the argument is a set of characters, so strip('mapS') and strip('Spam') give the same result " + S + " " + PSF + ".",
 "PrefixSuffixRemoval": "'Arthur: three!'.lstrip('Arthur: ') is 'ee!' because the argument is a set of characters, while .removeprefix('Arthur: ') is 'three!', 'report.txt'.removesuffix('.txt') is 'report' and 'report.txt'.removesuffix('.py') is unchanged; the chapter as read does not present them " + PSF + " " + S + ".",
 "Searching": "Finding and replacing text inside a string, which the chapter leaves to the course " + S + " " + PSF + ".",
 "FindAndCount": "'spam eggs spam'.find('spam') is 0, find('spam', 1) is 10, 'spam'.find('x') is -1, 'spam eggs spam'.count('spam') is 2, 'aaaa'.count('aa') is 2 because matches do not overlap and 'spam'.count('') is 5; the chapter as read does not present them " + S + " " + PSF + ".",
 "ReplaceMethod": "'spam, spam, spam'.replace('spam', 'eggs') is 'eggs, eggs, eggs', with a count of 1 it is 'eggs, spam, spam', and 'abc'.replace('b', '') is 'ac'; count can be a keyword since Python 3.13, and the chapter as read does not present it " + S + " " + PSF + ".",
 "CharactersAndBytes": "How text becomes numbers and bytes " + S + ".",
 "CodePointConversion": "Every character has a number in Unicode " + S + ".",
 "OrdAndChr": "ord('A') is 65, ord('4') is 52, ord('!') is 33, chr(65) is 'A', ord('A') < ord('B') is True and chr(ord('A') + 1) is 'B' " + S + "; ord of the euro sign is 8364, ord of the snake emoji is 128013, chr() accepts only 0 to 0x10FFFF and raises ValueError above it, and ord('ab') raises TypeError " + PSF + ".",
 "TextEncodings": "Encoding and decoding turn text into bytes and back " + S + ".",
 "Utf8Encoding": "'caf\\xe9'.encode('utf-8') is b'caf\\xc3\\xa9', so four characters are five bytes and decoding returns the original; the snake emoji is one character and four bytes in UTF-8 and in UTF-16 " + PSF + "; the chapter says 'utf-8' is the correct choice 99 percent of the time and points to Ned Batchelder's talk and a Computerphile video " + S + ".",
 "EncodeDecodeErrors": "Encoding 'caf\\xe9' as ascii raises UnicodeEncodeError: 'ascii' codec can't encode character '\\xe9' in position 3, decoding b'caf\\xc3' as utf-8 raises UnicodeDecodeError, errors='replace' gives b'caf?', 'backslashreplace' gives b'caf\\\\xe9' and 'ignore' gives b'caf', and decoding UTF-8 bytes as latin-1 succeeds but gives the wrong text; the chapter as read does not present them " + PSF + " " + S + ".",
 "FileEncoding": "Writing 'caf\\xe9' through a text wrapper with encoding='utf-8' leaves b'caf\\xc3\\xa9'; open() without encoding uses the locale encoding in Python 3.14.4, so a file written as UTF-8 was read back in a child process with the C locale and UTF-8 mode off under the ascii codec, which raised UnicodeDecodeError, while encoding='utf-8' read it correctly; PEP 686 makes UTF-8 mode the default from Python 3.15 " + PSF + " " + IN + "; the chapter as read mentions files only as the place where encoding happens " + S + ".",
 "ClipboardAndPrograms": "The chapter's programs work on text from the clipboard and from the user " + S + ".",
 "ClipboardPrograms": "The clipboard lets a program receive and hand over large text " + S + ".",
 "ClipboardModule": "pyperclip.copy('Hello, world!') and pyperclip.paste() send text to and receive text from the clipboard, and the module does not come with Python, so importing it on the build machine raised ModuleNotFoundError: No module named 'pyperclip' " + S + "; the clipboard itself was not executed here, and the chapter's programs were run against a stand-in module that keeps the text in a variable " + S + ".",
 "ProjectPrograms": "The chapter's clipboard projects, its Pig Latin program and its practice program " + S + ".",
 "BulletPointAdder": "Run unchanged against a stand-in clipboard, bulletPointAdder.py turns the four lines from Lists of animals to Lists of cultivars into the four lines with a star and a space in front, as printed; it loops with range(len(lines)) and joins with '\\n'.join(lines), and its step 2 listing ends with pyperclip.copy(text) on the unchanged text, which step 3 corrects by joining the lines " + S + "; with Windows line ends split('\\n') leaves a carriage return in every line and a trailing newline gives a final line holding only a star, where splitlines() does not " + PSF + ".",
 "AlternatingText": "Run unchanged against a stand-in clipboard, alternatingText.py turns 'Hello, world!' into 'hElLo, WoRlD!' by switching on every character, spaces included; on the chapter's sentence the result begins iF YoU CoPy sOmE TeXt and ends with tHiS:, whereas the chapter prints a version that ends with ThIs: and has a line break inside, so its printed output was not reproduced and the cause was not established " + S + ".",
 "InputValidation": "validateInput.py printed exactly the prompts the chapter shows for the inputs forty two, 42, secr3t! and secr3t: it rejected the first, accepted the second, rejected the third and accepted the fourth " + S + "; because isdecimal() accepts Arabic-Indic digits and isalnum() accepts accented letters, an age check with int() and a letters-and-numbers rule need isascii() where only ASCII is meant " + PSF + ".",
 "PigLatin": "Run unchanged, pigLat.py prints Ymay amenay isyay ALYAY EIGARTSWAY andyay Iyay amyay 4,000 yearsyay oldyay. for the chapter's message, whose split() gives eleven words; it treats y as a vowel, so years becomes yearsyay and rhythm becomes ythmrhay, it loses the capital of a word such as It's because istitle() is False for it, giving it'syay, and it treats an accented e as a consonant, so a word starting with one is moved, which the chapter as read does not say; the walk-through line with += shows seven exclamation marks for Wait!!! where the listing keeps three " + S + " " + PSF + ".",
 "TablePrinter": "The chapter asks for printTable(tableData) for three lists of four strings with right-justified columns, and a solution that finds the widths [8, 5, 5] with a loop and prints ' ' + item.rjust(width) for each cell prints the four lines of the chapter's table exactly; the chapter ends with 10 practice questions and this one practice program " + S + ".",
}
BEH = [
 ["the chapter's printed quote, escape and raw-string examples reproduce", r'''spam = "That is Alice's cat."
print(spam)
print('Say hi to Bob\'s mother.')
print("Hello there!\nHow are you?\nI\'m doing fine.")
print(r'The file is in C:\Users\Alice\Desktop')
print('Hello...\n\n...world!')
print(r'Hello...\n\n...world!')
print(len('\n'), len(r'\n'))''', "That is Alice's cat.\nSay hi to Bob's mother.\nHello there!\nHow are you?\nI'm doing fine.\nThe file is in C:\\Users\\Alice\\Desktop\nHello...\n\n...world!\nHello...\\n\\n...world!\n1 2"],
 ['a multiline string prints the same text as the escaped one (feedcat.py)', r'''a = """Dear Alice,

Can you feed Eve's cat this weekend?

Sincerely,
Bob"""
b = "Dear Alice,\n\nCan you feed Eve's cat this weekend?\n\nSincerely,\nBob"
print(a == b, a.count('\n'))
print(a.splitlines()[2])''', "True 5\nCan you feed Eve's cat this weekend?"],
 ["escape sequences beyond the chapter's table, and the backslash that stays", r'''print(repr('\x41\101\u00e9\N{SNAKE}'.encode('ascii', 'backslashreplace').decode()))
print(repr('a\
b'), repr('\a\b\f\r\v'))
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    code = compile("x = '\\q'", 'x', 'exec')
print(w[0].category.__name__, len(w))
ns = {}
exec(code, ns)
print(list(ns['x']))''', "'AA\\\\xe9\\\\U0001f40d'\n'ab' '\\x07\\x08\\x0c\\r\\x0b'\nSyntaxWarning 1\n['\\\\', 'q']"],
 ["the chapter's string-indexing and slicing examples reproduce", r'''greeting = 'Hello, world!'
print(greeting[0], greeting [4], greeting[-1], greeting[0:5], greeting[:5], greeting[7:-1], greeting[7:])
greeting_slice = greeting[0:5]
print(greeting_slice, greeting)
try:
    greeting[13]
except IndexError as e:
    print(type(e).__name__ + ': ' + str(e))
print(greeting[7:99], repr(greeting[99:]))''', "H o ! Hello Hello world world!\nHello Hello, world!\nIndexError: string index out of range\nworld! ''"],
 ['strings cannot be changed, and do not mix with numbers', r'''name = 'Zophie a cat'
try:
    name[7] = 'the'
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print(name[0:7] + 'the' + name[8:12])
try:
    'age ' + 4000
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print('age ' + str(4000))''', 'TypeError: \'str\' object does not support item assignment\nZophie the cat\nTypeError: can only concatenate str (not "int") to str\nage 4000'],
 ["the chapter's in and not in examples reproduce", r'''print('Hello' in 'Hello, World', 'Hello' in 'Hello', 'HELLO' in 'Hello, World', '' in 'spam', 'cats' not in 'cats and dogs')''', 'True True False True False'],
 ["the chapter's f-string, percent and format() examples reproduce", r'''name = 'Al'
age = 4000
print('Hello, my name is ' + name + '. I am ' + str(age) + ' years old.')
print('In ten years I will be ' + str(age + 10))
print(f'My name is {name}. I am {age} years old.')
print(f'In ten years I will be {age + 10}')
name = 'Zophie'
print(f'{name}', f'{{name}}')
name = 'Al'
print('My name is %s. I am %s years old.' % (name, age))
print('In ten years I will be %s' % (age + 10))
print('My name is {}. I am {} years old.'.format(name, age))
print('{1} years ago, {0} was born and named {0}.'.format(name, age))''', 'Hello, my name is Al. I am 4000 years old.\nIn ten years I will be 4010\nMy name is Al. I am 4000 years old.\nIn ten years I will be 4010\nZophie {name}\nMy name is Al. I am 4000 years old.\nIn ten years I will be 4010\nMy name is Al. I am 4000 years old.\n4000 years ago, Al was born and named Al.'],
 ['an f-string calls format() with the specifier, not only str()', r'''class Celsius:
    def __init__(self, degrees): self.degrees = degrees
    def __str__(self): return 'str:%s' % self.degrees
    def __format__(self, spec): return 'format:%s:%s' % (self.degrees, spec)
c = Celsius(21)
print(f'{c}', f'{c:.1f}', f'{c!s}', str(c), format(c, ''))
print(f'{3.14159:.2f}', format(3.14159, '.2f'))''', 'format:21: format:21:.1f str:21 str:21 format:21:\n3.14 3.14'],
 ['f-string alignment equals the justify methods; centering is lopsided by one', r'''s = 'Hello'
print(f'{s:>10}' == s.rjust(10), f'{s:<10}' == s.ljust(10), f'{s:^20}' == s.center(20), f'{s:*^20}' == s.center(20, '*'))
print(repr(s.center(20)))
print(s.center(20).index('H'), 20 - len(s.center(20).rstrip()))
try:
    s.rjust(10, '**')
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print(repr(s.rjust(3)), '42'.zfill(5), '-42'.zfill(5))''', "True True True True\n'       Hello        '\n7 8\nTypeError: The fill character must be exactly one character long\n'Hello' 00042 -0042"],
 ['Python 3.12 lets an f-string reuse its quote and hold a backslash in a field', r'''d = {'key': 7}
print(f"value {d["key"]}", f'{"-".join(["a", "b"])}', f"{'\n'.join(['x', 'y'])}")''', 'value 7 a-b x\ny'],
 ['the percent operator mistakes a tuple for its argument list', r'''try:
    print('%s' % (1, 2))
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print('%s' % ((1, 2),), '%s and %s' % ('a', 'b'))
try:
    print('{} {}'.format('one'))
except IndexError as e:
    print(type(e).__name__ + ': ' + str(e))
from string import Template
print(Template('$who likes $what').substitute(who='tim', what='kung pao'))''', 'TypeError: not all arguments converted during string formatting\n(1, 2) a and b\nIndexError: Replacement index 1 out of range for positional args tuple\ntim likes kung pao'],
 ['a t-string is a Template, not a str, and code can process its parts (Python 3.14)', r'''from string.templatelib import Template, Interpolation
import html
name = 'Al'
age = 4000
t = t'Hello {name}, you are {age:>6} years old.'
print(type(t).__name__, isinstance(t, str), t.strings)
print([(i.expression, i.value, i.conversion, repr(i.format_spec)) for i in t.interpolations])
def render(template):
    return ''.join(p if isinstance(p, str) else html.escape(str(p.value)) for p in template)
evil = '<b>x</b>'
print(render(t'<p>{evil}</p>'), f'<p>{evil}</p>')''', 'Template False (\'Hello \', \', you are \', \' years old.\')\n[(\'name\', \'Al\', None, "\'\'"), (\'age\', 4000, None, "\'>6\'")]\n<p>&lt;b&gt;x&lt;/b&gt;</p> <p><b>x</b></p>'],
 ['case methods return new strings; upper can lengthen a string; casefold is for caseless matching', r'''spam = 'Hello, world!'
up = spam.upper()
print(spam, up)
feeling = 'GREat'
print(feeling.lower() == 'great', 'GREat' == 'great')
print(len('stra\xdfe'), len('stra\xdfe'.upper()), 'stra\xdfe'.upper() == 'STRASSE')
print('STRASSE'.lower() == 'stra\xdfe'.lower(), 'STRASSE'.casefold() == 'stra\xdfe'.casefold())
print('Hello'.upper().lower().upper(), 'HELLO'.lower().islower())
print('they\'re bill\'s'.title(), __import__('string').capwords('they\'re bill\'s'))''', "Hello, world! HELLO, WORLD!\nTrue False\n6 7 True\nFalse True\nHELLO True\nThey'Re Bill'S They're Bill's"],
 ["the chapter's isX examples reproduce, and the methods are Unicode-aware", r'''print('hello'.isalpha(), 'hello123'.isalpha(), 'hello123'.isalnum(), 'hello'.isalnum(), '123'.isdecimal(), '    '.isspace(), 'This Is Title Case'.istitle())
print(''.isalpha(), ''.isdecimal(), ''.isspace(), ''.isupper(), ''.istitle())
print('\u3000'.isspace(), '\xa0'.isspace(), '\u0663\u0664'.isdecimal(), int('\u0663\u0664'))
print('\xb2'.isdecimal(), '\xb2'.isdigit(), '\xb2'.isnumeric())
try:
    int('\xb2')
except ValueError as e:
    print(type(e).__name__)
print('caf\xe9'.isalnum(), 'caf\xe9'.isascii(), 'cafe'.isascii())''', 'True False True True True True True\nFalse False False False False\nTrue True True 34\nFalse True True\nValueError\nTrue False True'],
 ['validateInput.py of the chapter prints what the chapter shows', r'''import subprocess, sys
prog = """while True:
    print('Enter your age:')
    age = input()
    if age.isdecimal():
        break
    print('Please enter a number for your age.')

while True:
    print('Select a new password (letters and numbers only):')
    password = input()
    if password.isalnum():
        break
    print('Passwords can only have letters and numbers.')
"""
r = subprocess.run([sys.executable, '-c', prog], input='forty two\n42\nsecr3t!\nsecr3t\n', capture_output=True, text=True)
print(r.stdout, end='')
print(r.returncode)''', 'Enter your age:\nPlease enter a number for your age.\nEnter your age:\nSelect a new password (letters and numbers only):\nPasswords can only have letters and numbers.\nSelect a new password (letters and numbers only):\n0'],
 ['startswith and endswith take a tuple; join needs strings; split has two algorithms', r'''print('Hello, world!'.startswith('Hello'), 'Hello, world!'.endswith('world!'), 'abc123'.startswith('abcdef'), 'abc123'.endswith('12'))
print('notes.txt'.endswith(('.py', '.txt')), 'https://x'.startswith(('http://', 'https://')))
try:
    ', '.join([1, 2])
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print(', '.join(('a', 'b')), '-'.join('Python'), ','.join(str(n) for n in range(3)))
print(' a  b '.split(), ' a  b '.split(' '), 'a,b,c'.split(',', 1), 'a b c'.split(maxsplit=1))
spam = """Dear Alice,
There is a milk bottle in the fridge
that is labeled "Milk Experiment."

Please do not drink it.
Sincerely,
Bob"""
print(spam.split('\n'))''', 'True True False False\nTrue True\nTypeError: sequence item 0: expected str instance, int found\na, b P-y-t-h-o-n 0,1,2\n[\'a\', \'b\'] [\'\', \'a\', \'\', \'b\', \'\'] [\'a\', \'b,c\'] [\'a\', \'b c\']\n[\'Dear Alice,\', \'There is a milk bottle in the fridge\', \'that is labeled "Milk Experiment."\', \'\', \'Please do not drink it.\', \'Sincerely,\', \'Bob\']'],
 ["the chapter's justify, center and strip examples reproduce with the right widths", r'''print(repr('Hello'.rjust(10)), repr('Hello'.ljust(10)))
print(repr('Hello'.rjust(20, '*')), repr('Hello'.ljust(20, '-')))
print(repr('Hello'.center(20)), repr('Hello'.center(20, '=')))
spam = '    Hello, World    '
print(repr(spam.strip()), repr(spam.lstrip()), repr(spam.rstrip()))
spam = 'SpamSpamBaconSpamEggsSpamSpam'
print(spam.strip('ampS'), spam.strip('mapS'), spam.strip('Spam'))''', "'     Hello' 'Hello     '\n'***************Hello' 'Hello---------------'\n'       Hello        ' '=======Hello========'\n'Hello, World' 'Hello, World    ' '    Hello, World'\nBaconSpamEggs BaconSpamEggs BaconSpamEggs"],
 ['the chapter prints 14 spaces before Hello and 9 before Hello, World for rjust(20); Python 3.14.4 gives 15 and 8', r'''a = 'Hello'.rjust(20)
b = 'Hello, World'.rjust(20)
print(len(a) - len(a.lstrip()), len(a), len(b) - len(b.lstrip()), len(b))
chapter_a = "'" + ' ' * 14 + "Hello'"
chapter_b = "'" + ' ' * 9 + "Hello, World'"
print(len(eval(chapter_a)), len(eval(chapter_b)), eval(chapter_a) == a, eval(chapter_b) == b)''', '15 20 8 20\n19 21 False False'],
 ['strip removes a set of characters, not a prefix; removeprefix removes one', r'''s = 'Arthur: three!'
print(s.lstrip('Arthur: '), s.removeprefix('Arthur: '))
print('Monty Python'.rstrip(' Python'), 'Monty Python'.removesuffix(' Python'))
print('BaseTestCase'.removeprefix('Test'), 'TestHook'.removeprefix('Test'))''', 'ee! three!\nM Monty\nBaseTestCase Hook'],
 ["split('\\n') leaves a carriage return on Windows-style text; splitlines does not", r'''text = 'Lists of animals\r\nLists of cultivars\r\n'
print(text.split('\n'))
print(text.splitlines())
print(repr('\n'.join('* ' + line for line in text.split('\n'))))
print(repr('\n'.join('* ' + line for line in text.splitlines())))
print('a\x0bb\x1cc\u2028d'.splitlines())''', "['Lists of animals\\r', 'Lists of cultivars\\r', '']\n['Lists of animals', 'Lists of cultivars']\n'* Lists of animals\\r\\n* Lists of cultivars\\r\\n* '\n'* Lists of animals\\n* Lists of cultivars'\n['a', 'b', 'c', 'd']"],
 ['ord, chr and the range of code points', r'''print(ord('A'), ord('4'), ord('!'), chr(65))
print(ord('B'), ord('A') < ord('B'), chr(ord('A')), chr(ord('A') + 1))
print(ord('\u20ac'), chr(8364) == '\u20ac', ord('\U0001f40d'), hex(ord('\U0001f40d')))
try:
    chr(0x110000)
except ValueError as e:
    print(type(e).__name__ + ': ' + str(e))
try:
    ord('ab')
except TypeError as e:
    print(type(e).__name__ + ': ' + str(e))
print(len('\U0001f40d'), len('\U0001f40d'.encode('utf-8')), len('\U0001f40d'.encode('utf-16-le')))''', '65 52 33 A\n66 True A B\n8364 True 128013 0x1f40d\nValueError: chr() arg not in range(0x110000)\nTypeError: ord() expected a character, but string of length 2 found\n1 4 4'],
 ['encoding turns text into bytes and back; the wrong codec raises or garbles', r'''s = 'caf\xe9'
b = s.encode('utf-8')
print(b, len(s), len(b), b.decode('utf-8') == s)
print(s.encode('latin-1'), ascii(b.decode('latin-1')))
try:
    s.encode('ascii')
except UnicodeEncodeError as e:
    print(type(e).__name__ + ': ' + str(e))
try:
    b'caf\xc3'.decode('utf-8')
except UnicodeDecodeError as e:
    print(type(e).__name__ + ': ' + str(e))
print(s.encode('ascii', errors='replace'), s.encode('ascii', errors='backslashreplace'), s.encode('ascii', errors='ignore'))''', "b'caf\\xc3\\xa9' 4 5 True\nb'caf\\xe9' 'caf\\xc3\\xa9'\nUnicodeEncodeError: 'ascii' codec can't encode character '\\xe9' in position 3: ordinal not in range(128)\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 3: unexpected end of data\nb'caf?' b'caf\\\\xe9' b'caf'"],
 ['open() without encoding follows the locale, not UTF-8 (Python 3.14)', r'''import os, subprocess, sys, tempfile
path = os.path.join(tempfile.mkdtemp(), 'note.txt')
with open(path, 'w', encoding='utf-8') as f:
    f.write('caf\xe9')
print(open(path, 'rb').read())
child = "import sys\nprint(sys.flags.utf8_mode, open(%r).encoding)\ntry:\n    print(open(%r).read())\nexcept UnicodeDecodeError as e:\n    print(type(e).__name__ + ': ' + str(e))\nprint(open(%r, encoding='utf-8').read() == 'caf\\xe9')" % (path, path, path)
env = dict(os.environ, LC_ALL='C', PYTHONCOERCECLOCALE='0')
env.pop('PYTHONUTF8', None)
r = subprocess.run([sys.executable, '-X', 'utf8=0', '-c', child], env=env, capture_output=True, text=True)
print(r.stdout, end='')''', "b'caf\\xc3\\xa9'\n0 ANSI_X3.4-1968\nUnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)\nTrue"],
 ['bulletPointAdder.py and alternatingText.py of the chapter run unchanged against a stand-in clipboard module', r'''import sys, types
clip = {'text': ''}
fake = types.ModuleType('pyperclip')
fake.copy = lambda s: clip.__setitem__('text', s)
fake.paste = lambda: clip['text']
sys.modules['pyperclip'] = fake
bullets = """import pyperclip
text = pyperclip.paste()

# Separate lines and add stars.
lines = text.split('\\n')
for i in range(len(lines)):  # Loop through all indexes in the "lines" list.
    lines[i] = '* ' + lines[i]  # Add a star to each string in the "lines" list.
text = '\\n'.join(lines)
pyperclip.copy(text)
"""
clip['text'] = 'Lists of animals\nLists of aquarium life\nLists of biologists by author abbreviation\nLists of cultivars'
exec(bullets, {})
print(clip['text'])
alt = """import pyperclip

text = pyperclip.paste()  # Get the text off the clipboard.
alt_text = ''  # This string holds the alternating case.
make_uppercase = False
for character in text:
    # Go through each character and add it to alt_text:
    if make_uppercase:
        alt_text += character.upper()
    else:
        alt_text += character.lower()

    # Set make_uppercase to its opposite value:
    make_uppercase = not make_uppercase
pyperclip.copy(alt_text)  # Put the result on the clipboard.
print(alt_text)  # Print the result on the screen too.
"""
clip['text'] = 'If you copy some text to the clipboard (for instance, this sentence) and run this program, the output and clipboard contents become this:'
exec(alt, {})
print(clip['text'].split()[-1], 'ThIs:' == clip['text'].split()[-1])''', '* Lists of animals\n* Lists of aquarium life\n* Lists of biologists by author abbreviation\n* Lists of cultivars\niF YoU CoPy sOmE TeXt tO ThE ClIpBoArD (fOr iNsTaNcE, tHiS SeNtEnCe) AnD RuN ThIs pRoGrAm, ThE OuTpUt aNd cLiPbOaRd cOnTeNtS BeCoMe tHiS:\ntHiS: False'],
 ["pigLat.py of the chapter prints the chapter's translation", r'''import subprocess, sys
prog = """# English to pig latin
print('Enter the English message to translate into pig latin:')
message = input()

VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')

pig_latin = [] # A list of the words in pig latin
for word in message.split():
    # Separate the non-letters at the start of this word:
    prefix_non_letters = ''
    while len(word) > 0 and not word[0].isalpha():
        prefix_non_letters += word[0]
        word = word[1:]
    if len(word) == 0:
        pig_latin.append(prefix_non_letters)
        continue

    # Separate the non-letters at the end of this word:
    suffix_non_letters = ''
    while not word[-1].isalpha():
        suffix_non_letters = word[-1] + suffix_non_letters
        word = word[:-1]

    # Remember if the word was in uppercase or title case:
    was_upper = word.isupper()
    was_title = word.istitle()

    word = word.lower() # Make the word lowercase for translation.

    # Separate the consonants at the start of this word:
    prefix_consonants = ''
    while len(word) > 0 and not word[0] in VOWELS:
        prefix_consonants += word[0]
        word = word[1:]

    # Add the pig latin ending to the word:
    if prefix_consonants != '':
        word += prefix_consonants + 'ay'
    else:
        word += 'yay'

    # Set the word back to uppercase or title case:
    if was_upper:
        word = word.upper()
    if was_title:
        word = word.title()

    # Add the non-letters back to the start or end of the word.
    pig_latin.append(prefix_non_letters + word + suffix_non_letters)

# Join all the words back together into a single string:
print(' '.join(pig_latin))
"""
def pig(msg):
    r = subprocess.run([sys.executable, '-c', prog], input=msg + '\n', capture_output=True, text=True)
    return r.stdout.split('\n')[1]
print(pig('My name is AL SWEIGART and I am 4,000 years old.'))
print(pig("It's a rhythm, hmm... yes (okay) Wait!!! \xe9cole"))''', "Ymay amenay isyay ALYAY EIGARTSWAY andyay Iyay amyay 4,000 yearsyay oldyay.\nit'syay ayay ythmrhay, hmmay... yesyay (okayyay) Aitway!!! oleécay"],
 ['the pig latin walk-through line with += doubles the stored suffix', r'''def listing(word):
    suffix = ''
    while not word[-1].isalpha():
        suffix = word[-1] + suffix
        word = word[:-1]
    return word, suffix
def walkthrough(word):
    suffix = ''
    while not word[-1].isalpha():
        suffix += word[-1] + suffix
        word = word[:-1]
    return word, suffix
print(listing('old.'), walkthrough('old.'))
print(listing('Wait!!!'), walkthrough('Wait!!!'))
print(listing('hi?!'), walkthrough('hi?!'))''', "('old', '.') ('old', '.')\n('Wait', '!!!') ('Wait', '!!!!!!!')\n('hi', '?!') ('hi', '!?!')"],
 ["the practice program: printTable prints the chapter's table", r'''tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]
def printTable(table):
    colWidths = [0] * len(table)
    for i in range(len(table)):
        for item in table[i]:
            if len(item) > colWidths[i]:
                colWidths[i] = len(item)
    for row in range(len(table[0])):
        for col in range(len(table)):
            print(' ' + table[col][row].rjust(colWidths[col]), end='')
        print()
printTable(tableData)
print([max(map(len, c)) for c in tableData])''', 'apples Alice  dogs\n  oranges   Bob  cats\n cherries Carol moose\n   banana David goose\n[8, 5, 5]'],
 ["the chapter's practice questions 6 to 8 give these values", r'''print('Hello, world!'[1], 'Hello, world!'[0:5], 'Hello, world!'[:5], 'Hello, world!'[3:])
print('Hello'.upper(), 'Hello'.upper().isupper(), 'Hello'.upper().lower())
print('Remember, remember, the fifth of November.'.split())
print('-'.join('There can be only one.'.split()))''', "e Hello Hello lo, world!\nHELLO True hello\n['Remember,', 'remember,', 'the', 'fifth', 'of', 'November.']\nThere-can-be-only-one."],
 ['pyperclip is not installed on the build machine, and t-strings are a SyntaxError in Python 3.13', r'''import subprocess, sys
try:
    import pyperclip
except ModuleNotFoundError as e:
    print(type(e).__name__ + ': ' + str(e))
r = subprocess.run(['/usr/bin/python3.13', '-c', "x = 'a'\nt = t'{x}'"], capture_output=True, text=True)
print(r.returncode, r.stderr.strip().splitlines()[-1])
r = subprocess.run(['/usr/bin/python3.13', '-c', "x = 'a'\nprint(f'{x!r:>5}')"], capture_output=True, text=True)
print(r.stdout.strip())''', "ModuleNotFoundError: No module named 'pyperclip'\n1 SyntaxError: invalid syntax\n'a'"],
]
